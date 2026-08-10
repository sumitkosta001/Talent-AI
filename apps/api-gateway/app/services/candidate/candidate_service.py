"""Candidate Profile Module Business Logic Service."""

import logging
from uuid import UUID
from datetime import datetime, timezone
from typing import Optional, List, Union

from app.models.candidate_profile import CandidateProfile
from app.models.candidate_education import CandidateEducation
from app.models.candidate_experience import CandidateExperience
from app.models.candidate_skill import CandidateSkill
from app.repositories.candidate.profile_repository import CandidateProfileRepository
from app.repositories.candidate.education_repository import EducationRepository
from app.repositories.candidate.experience_repository import ExperienceRepository
from app.repositories.candidate.skill_repository import SkillRepository
from app.schemas.candidate.profile import CandidateProfileUpdate
from app.schemas.candidate.education import EducationCreate, EducationUpdate
from app.schemas.candidate.experience import ExperienceCreate, ExperienceUpdate
from app.schemas.candidate.skill import SkillCreate, SkillUpdate
from app.exceptions.candidate import (
    CandidateProfileNotFoundError,
    EducationNotFoundError,
    ExperienceNotFoundError,
    SkillNotFoundError,
    DuplicateSkillError,
    InvalidDateRangeError,
)

logger = logging.getLogger("talentai.services.candidate")


class CandidateService:
    """Service encapsulating candidate profile, education, experience, and skill workflows."""

    def __init__(
        self,
        profile_repo: CandidateProfileRepository,
        education_repo: EducationRepository,
        experience_repo: ExperienceRepository,
        skill_repo: SkillRepository,
    ) -> None:
        self.profile_repo = profile_repo
        self.education_repo = education_repo
        self.experience_repo = experience_repo
        self.skill_repo = skill_repo

    def calculate_profile_completion(
        self,
        profile: CandidateProfile,
        education_list: List[CandidateEducation],
        experience_list: List[CandidateExperience],
        skill_list: List[CandidateSkill],
    ) -> int:
        """Centralized deterministic candidate profile completion calculator (0-100%)."""
        percentage = 0

        # Basic fields (Total 55%)
        if profile.phone_number and profile.phone_number.strip():
            percentage += 10
        if profile.location and profile.location.strip():
            percentage += 10
        if profile.headline and profile.headline.strip():
            percentage += 10
        if profile.bio and profile.bio.strip():
            percentage += 10
        if profile.profile_picture_url and profile.profile_picture_url.strip():
            percentage += 10
        if profile.linkedin_url and profile.linkedin_url.strip():
            percentage += 5
        if profile.github_url and profile.github_url.strip():
            percentage += 5
        if profile.portfolio_url and profile.portfolio_url.strip():
            percentage += 5

        # Child collections (Total 35%)
        if any(not edu.is_deleted for edu in education_list):
            percentage += 15
        if any(not exp.is_deleted for exp in experience_list):
            percentage += 10
        if any(not s.is_deleted for s in skill_list):
            percentage += 10

        return min(max(percentage, 0), 100)

    async def get_or_create_profile(self, user_id: UUID | str) -> CandidateProfile:
        """Retrieve a candidate's profile, automatically creating it if it doesn't exist."""
        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
            logger.info("Initializing new candidate profile for user: %s", user_id)
            new_profile = CandidateProfile(
                user_id=UUID(str(user_id)) if isinstance(user_id, str) else user_id,
                profile_completion_percentage=0,
            )
            profile = await self.profile_repo.create(new_profile)
        return profile

    async def update_profile(
        self, user_id: UUID | str, updates: CandidateProfileUpdate
    ) -> CandidateProfile:
        """Update a candidate's basic profile details and recalculate completion percentage."""
        profile = await self.get_or_create_profile(user_id)

        # Apply updates
        update_data = updates.model_dump(exclude_unset=True)
        name = update_data.pop("name", None)
        update_data.pop("email", None)

        for field, value in update_data.items():
            setattr(profile, field, value)

        if name is not None:
            name = name.strip()
            name_parts = name.split(None, 1)
            first_name = name_parts[0] if len(name_parts) > 0 else ""
            last_name = name_parts[1] if len(name_parts) > 1 else ""
            if profile.user:
                profile.user.first_name = first_name
                profile.user.last_name = last_name

        # Recalculate completion
        profile.profile_completion_percentage = self.calculate_profile_completion(
            profile, profile.education, profile.experience, profile.skills
        )

        updated_profile = await self.profile_repo.update(profile)
        logger.info("Updated candidate profile for user %s. Completion: %d%%", user_id, updated_profile.profile_completion_percentage)
        return updated_profile

    # ==========================================================================
    # EDUCATION HISTORY METHODS
    # ==========================================================================

    async def get_education_list(self, user_id: UUID | str) -> List[CandidateEducation]:
        """Fetch all active education records for the candidate."""
        profile = await self.get_or_create_profile(user_id)
        return await self.education_repo.list_by_profile_id(profile.id)

    async def add_education(self, user_id: UUID | str, data: EducationCreate) -> CandidateEducation:
        """Create a new education entry for the candidate's profile."""
        profile = await self.get_or_create_profile(user_id)

        new_education = CandidateEducation(
            candidate_profile_id=profile.id,
            degree=data.degree,
            institution=data.institution,
            start_date=data.start_date,
            end_date=data.end_date,
            grade_or_cgpa=data.grade_or_cgpa,
        )

        education = await self.education_repo.create(new_education)

        # Recalculate profile completion
        active_edu = await self.education_repo.list_by_profile_id(profile.id)
        profile.profile_completion_percentage = self.calculate_profile_completion(
            profile, active_edu, profile.experience, profile.skills
        )
        await self.profile_repo.update(profile)

        logger.info("Added education entry %s for user %s", education.id, user_id)
        return education

    async def update_education(
        self, user_id: UUID | str, education_id: UUID | str, data: EducationUpdate
    ) -> CandidateEducation:
        """Update an education entry, verifying candidate ownership to prevent IDOR."""
        profile = await self.get_or_create_profile(user_id)

        education = await self.education_repo.get_by_id_for_profile(education_id, profile.id)
        if not education:
            raise EducationNotFoundError(str(education_id))

        update_dict = data.model_dump(exclude_unset=True)

        # Validate start/end dates after merge
        new_start = update_dict.get("start_date", education.start_date)
        new_end = update_dict.get("end_date", education.end_date)
        if new_end and new_start > new_end:
            raise InvalidDateRangeError("Start date cannot be after end date.")

        for field, value in update_dict.items():
            setattr(education, field, value)

        updated_edu = await self.education_repo.update(education)

        # Recalculate profile completion
        active_edu = await self.education_repo.list_by_profile_id(profile.id)
        profile.profile_completion_percentage = self.calculate_profile_completion(
            profile, active_edu, profile.experience, profile.skills
        )
        await self.profile_repo.update(profile)

        logger.info("Updated education entry %s for user %s", education_id, user_id)
        return updated_edu

    async def delete_education(self, user_id: UUID | str, education_id: UUID | str) -> None:
        """Delete (soft delete) an education entry, verifying candidate ownership to prevent IDOR."""
        profile = await self.get_or_create_profile(user_id)

        education = await self.education_repo.get_by_id_for_profile(education_id, profile.id)
        if not education:
            raise EducationNotFoundError(str(education_id))

        await self.education_repo.delete(education)

        # Recalculate profile completion
        active_edu = await self.education_repo.list_by_profile_id(profile.id)
        profile.profile_completion_percentage = self.calculate_profile_completion(
            profile, active_edu, profile.experience, profile.skills
        )
        await self.profile_repo.update(profile)

        logger.info("Deleted education entry %s for user %s", education_id, user_id)

    # ==========================================================================
    # WORK EXPERIENCE HISTORY METHODS
    # ==========================================================================

    async def get_experience_list(self, user_id: UUID | str) -> List[CandidateExperience]:
        """Fetch all active experience records for the candidate."""
        profile = await self.get_or_create_profile(user_id)
        return await self.experience_repo.list_by_profile_id(profile.id)

    async def add_experience(self, user_id: UUID | str, data: ExperienceCreate) -> CandidateExperience:
        """Create a new experience entry for the candidate's profile."""
        profile = await self.get_or_create_profile(user_id)

        new_experience = CandidateExperience(
            candidate_profile_id=profile.id,
            company=data.company,
            job_title=data.job_title,
            start_date=data.start_date,
            end_date=data.end_date,
            description=data.description,
        )

        experience = await self.experience_repo.create(new_experience)

        # Recalculate profile completion
        active_exp = await self.experience_repo.list_by_profile_id(profile.id)
        profile.profile_completion_percentage = self.calculate_profile_completion(
            profile, profile.education, active_exp, profile.skills
        )
        await self.profile_repo.update(profile)

        logger.info("Added experience entry %s for user %s", experience.id, user_id)
        return experience

    async def update_experience(
        self, user_id: UUID | str, experience_id: UUID | str, data: ExperienceUpdate
    ) -> CandidateExperience:
        """Update an experience entry, verifying candidate ownership to prevent IDOR."""
        profile = await self.get_or_create_profile(user_id)

        experience = await self.experience_repo.get_by_id_for_profile(experience_id, profile.id)
        if not experience:
            raise ExperienceNotFoundError(str(experience_id))

        update_dict = data.model_dump(exclude_unset=True)

        # Validate start/end dates after merge
        new_start = update_dict.get("start_date", experience.start_date)
        new_end = update_dict.get("end_date", experience.end_date)
        if new_end and new_start > new_end:
            raise InvalidDateRangeError("Start date cannot be after end date.")

        for field, value in update_dict.items():
            setattr(experience, field, value)

        updated_exp = await self.experience_repo.update(experience)

        # Recalculate profile completion
        active_exp = await self.experience_repo.list_by_profile_id(profile.id)
        profile.profile_completion_percentage = self.calculate_profile_completion(
            profile, profile.education, active_exp, profile.skills
        )
        await self.profile_repo.update(profile)

        logger.info("Updated experience entry %s for user %s", experience_id, user_id)
        return updated_exp

    async def delete_experience(self, user_id: UUID | str, experience_id: UUID | str) -> None:
        """Delete (soft delete) an experience entry, verifying candidate ownership to prevent IDOR."""
        profile = await self.get_or_create_profile(user_id)

        experience = await self.experience_repo.get_by_id_for_profile(experience_id, profile.id)
        if not experience:
            raise ExperienceNotFoundError(str(experience_id))

        await self.experience_repo.delete(experience)

        # Recalculate profile completion
        active_exp = await self.experience_repo.list_by_profile_id(profile.id)
        profile.profile_completion_percentage = self.calculate_profile_completion(
            profile, profile.education, active_exp, profile.skills
        )
        await self.profile_repo.update(profile)

        logger.info("Deleted experience entry %s for user %s", experience_id, user_id)

    # ==========================================================================
    # SKILLS MANAGEMENT METHODS
    # ==========================================================================

    async def get_skills_list(self, user_id: UUID | str) -> List[CandidateSkill]:
        """Fetch all active skills for the candidate."""
        profile = await self.get_or_create_profile(user_id)
        return await self.skill_repo.list_by_profile_id(profile.id)

    async def add_skill(self, user_id: UUID | str, data: SkillCreate) -> CandidateSkill:
        """Add a new skill, ensuring uniqueness and preventing duplicates for this candidate."""
        profile = await self.get_or_create_profile(user_id)

        normalized = data.skill_name.strip().lower()

        # Check for duplicates on active skills
        existing = await self.skill_repo.get_by_normalized_name(profile.id, normalized)
        if existing:
            raise DuplicateSkillError(data.skill_name)

        new_skill = CandidateSkill(
            candidate_profile_id=profile.id,
            skill_name=data.skill_name,
            normalized_skill_name=normalized,
            category=data.category,
            proficiency=data.proficiency,
        )

        skill = await self.skill_repo.create(new_skill)

        # Recalculate profile completion
        active_skills = await self.skill_repo.list_by_profile_id(profile.id)
        profile.profile_completion_percentage = self.calculate_profile_completion(
            profile, profile.education, profile.experience, active_skills
        )
        await self.profile_repo.update(profile)

        logger.info("Added skill entry %s (%s) for user %s", skill.id, skill.skill_name, user_id)
        return skill

    async def update_skill(
        self, user_id: UUID | str, skill_id: UUID | str, data: SkillUpdate
    ) -> CandidateSkill:
        """Update skill details (e.g. proficiency or category), preventing duplicates on rename."""
        profile = await self.get_or_create_profile(user_id)

        skill = await self.skill_repo.get_by_id_for_profile(skill_id, profile.id)
        if not skill:
            raise SkillNotFoundError(str(skill_id))

        update_dict = data.model_dump(exclude_unset=True)

        # Handle skill rename duplicate check
        if "skill_name" in update_dict:
            new_name = update_dict["skill_name"].strip()
            normalized = new_name.lower()
            if normalized != skill.normalized_skill_name:
                existing = await self.skill_repo.get_by_normalized_name(profile.id, normalized)
                if existing:
                    raise DuplicateSkillError(new_name)
                skill.skill_name = new_name
                skill.normalized_skill_name = normalized

        # Update other fields
        if "category" in update_dict:
            skill.category = update_dict["category"]
        if "proficiency" in update_dict:
            skill.proficiency = update_dict["proficiency"]

        updated_skill = await self.skill_repo.update(skill)

        # Recalculate profile completion
        active_skills = await self.skill_repo.list_by_profile_id(profile.id)
        profile.profile_completion_percentage = self.calculate_profile_completion(
            profile, profile.education, profile.experience, active_skills
        )
        await self.profile_repo.update(profile)

        logger.info("Updated skill entry %s for user %s", skill_id, user_id)
        return updated_skill

    async def delete_skill(self, user_id: UUID | str, skill_id: UUID | str) -> None:
        """Delete (soft delete) a skill entry, verifying candidate ownership to prevent IDOR."""
        profile = await self.get_or_create_profile(user_id)

        skill = await self.skill_repo.get_by_id_for_profile(skill_id, profile.id)
        if not skill:
            raise SkillNotFoundError(str(skill_id))

        await self.skill_repo.delete(skill)

        # Recalculate profile completion
        active_skills = await self.skill_repo.list_by_profile_id(profile.id)
        profile.profile_completion_percentage = self.calculate_profile_completion(
            profile, profile.education, profile.experience, active_skills
        )
        await self.profile_repo.update(profile)

        logger.info("Deleted skill entry %s for user %s", skill_id, user_id)
