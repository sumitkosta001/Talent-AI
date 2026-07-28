import React from 'react';
import { Skill } from '../../types/resume';
import SkillBadge from './SkillBadge';

interface SkillSectionProps {
  skills: Skill[];
  missingSkills?: Skill[];
}

export default function SkillSection({ skills, missingSkills = [] }: SkillSectionProps) {
  const categories = {
    technical: skills.filter((s) => s.type === 'technical'),
    framework: skills.filter((s) => s.type === 'framework'),
    tool: skills.filter((s) => s.type === 'tool'),
    soft: skills.filter((s) => s.type === 'soft'),
  };

  const renderGroup = (label: string, items: Skill[], isMissing = false) => {
    if (items.length === 0) return null;
    return (
      <div className="space-y-2">
        <h4 className="text-xs font-semibold text-[#64748B] uppercase tracking-wider">{label}</h4>
        <div className="flex flex-wrap gap-2">
          {items.map((item, idx) => (
            <SkillBadge key={idx} skill={item} isMissing={isMissing} />
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-4">
      {renderGroup('Technical Languages', categories.technical)}
      {renderGroup('Frameworks & Libraries', categories.framework)}
      {renderGroup('Developer Tools & Databases', categories.tool)}
      {renderGroup('Soft Skills & Methodologies', categories.soft)}
      {missingSkills.length > 0 && renderGroup('Missing Core Skills', missingSkills, true)}
    </div>
  );
}
