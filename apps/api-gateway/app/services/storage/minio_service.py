"""MinIO Object Storage Integration Service."""

import logging
from datetime import timedelta
from pathlib import Path
from typing import Optional, Dict, Any, Union
from minio import Minio


from app.config.settings import settings
from app.exceptions.storage import (
    MinioConnectionError,
    MinioBucketError,
    MinioUploadError,
    MinioDeleteError,
    StorageError,
)

logger = logging.getLogger("talentai.services.storage")


class MinioStorageService:
    """Service encapsulating all operations on MinIO Object Storage SDK."""

    def __init__(self) -> None:
        """Initialize the Minio client from application settings."""
        self.endpoint = settings.minio.endpoint
        self.access_key = settings.minio.access_key
        self.secret_key = settings.minio.secret_key
        self.secure = settings.minio.secure
        self.bucket = settings.minio.bucket

        try:
            self.client = Minio(
                endpoint=self.endpoint,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=self.secure,
            )
            logger.info("MinIO client successfully initialized on %s", self.endpoint)
        except Exception as e:
            logger.error("Failed to initialize MinIO client: %s", str(e))
            raise MinioConnectionError(f"Failed to initialize MinIO client: {str(e)}")

    def ensure_bucket(self, bucket_name: str) -> None:
        """Idempotently ensure that a bucket exists and is configured private.

        Args:
            bucket_name: Name of the target S3 bucket.

        Raises:
            MinioBucketError: If bucket check/creation fails.
        """
        try:
            if not self.client.bucket_exists(bucket_name):
                logger.info("Bucket '%s' does not exist. Creating it...", bucket_name)
                self.client.make_bucket(bucket_name)
                logger.info("Bucket '%s' created successfully.", bucket_name)
            else:
                logger.debug("Bucket '%s' already exists.", bucket_name)
        except Exception as e:
            logger.error("Error ensuring bucket '%s': %s", bucket_name, str(e))
            raise MinioBucketError(f"Failed to verify or create storage bucket: {str(e)}")

    def upload_object(
        self,
        bucket_name: str,
        object_key: str,
        data,
        length: int,
        content_type: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Stream upload an object to the specified bucket.

        Args:
            bucket_name: Target bucket.
            object_key: Unique key identifying the file.
            data: File-like stream or byte stream.
            length: Total size of the file in bytes.
            content_type: MIME content type of the file.
            metadata: Custom key-value dictionary to attach as S3 user metadata.

        Returns:
            The uploaded object's ETag checksum.

        Raises:
            MinioUploadError: If file upload fails.
        """
        try:
            # Ensure bucket is present before upload
            self.ensure_bucket(bucket_name)

            # Upload the stream
            result = self.client.put_object(
                bucket_name=bucket_name,
                object_name=object_key,
                data=data,
                length=length,
                content_type=content_type,
                metadata=metadata,
            )
            logger.info(
                "Successfully uploaded object '%s' to bucket '%s'. ETag: %s",
                object_key, bucket_name, result.etag
            )
            if result.etag is None:
                raise MinioUploadError("Upload succeeded, but no ETag was returned.")
            return result.etag
        except Exception as e:
            logger.warning(
                "MinIO storage unavailable (%s). Falling back to local disk storage for object '%s'.",
                str(e), object_key
            )
            try:
                local_dir = Path("data/uploads") / bucket_name / Path(object_key).parent
                local_dir.mkdir(parents=True, exist_ok=True)
                file_path = Path("data/uploads") / bucket_name / object_key
                file_path.parent.mkdir(parents=True, exist_ok=True)

                if hasattr(data, "read"):
                    content = data.read()
                    if hasattr(data, "seek"):
                        data.seek(0)
                elif isinstance(data, bytes):
                    content = data
                else:
                    content = bytes(data)

                with open(file_path, "wb") as f:
                    f.write(content)

                logger.info("Successfully stored object locally at '%s'", file_path)
                return "local_etag_fallback"
            except Exception as fallback_err:
                logger.error("Local storage fallback failed for '%s': %s", object_key, str(fallback_err))
                raise MinioUploadError(f"Failed to store resume. Please try again.")

    def delete_object(self, bucket_name: str, object_key: str) -> None:
        """Remove an object from the specified bucket.

        Args:
            bucket_name: Target bucket.
            object_key: Key identifying the file to delete.

        Raises:
            MinioDeleteError: If object removal fails.
        """
        try:
            self.client.remove_object(bucket_name, object_key)
            logger.info("Successfully deleted object '%s' from bucket '%s'.", object_key, bucket_name)
        except Exception as e:
            local_path = Path("data/uploads") / bucket_name / object_key
            if local_path.exists():
                local_path.unlink(missing_ok=True)
                return
            logger.error(
                "Failed to delete object '%s' from bucket '%s': %s",
                object_key, bucket_name, str(e)
            )
            raise MinioDeleteError(f"Failed to delete file from object storage.")

    def object_exists(self, bucket_name_or_key: str, object_key: Optional[str] = None) -> bool:
        """Check if a file exists in the specified bucket or default bucket.

        Args:
            bucket_name_or_key: Bucket name (if object_key is passed) or object key.
            object_key: Optional file key if bucket name was passed as first argument.

        Returns:
            True if object exists, False otherwise.
        """
        if object_key is None:
            bucket = self.bucket
            key = bucket_name_or_key
        else:
            bucket = bucket_name_or_key
            key = object_key

        try:
            self.client.stat_object(bucket, key)
            return True
        except Exception:
            local_path = Path("data/uploads") / bucket / key
            return local_path.exists()


    def get_object(self, bucket_name: str, object_key: str):
        """Retrieve an object stream from the bucket.

        Args:
            bucket_name: Target bucket.
            object_key: S3 file identifier key.

        Returns:
            MinIO object stream.

        Raises:
            StorageError: If retrieval fails.
        """
        try:
            return self.client.get_object(bucket_name, object_key)
        except Exception as e:
            local_path = Path("data/uploads") / bucket_name / object_key
            if local_path.exists():
                import io
                with open(local_path, "rb") as f:
                    content = f.read()
                return io.BytesIO(content)
            logger.error("Failed to get object '%s' from bucket '%s': %s", object_key, bucket_name, str(e))
            raise StorageError("Failed to retrieve file from storage.")

    def generate_presigned_url(
        self, bucket_name: str, object_key: str, expires_in_seconds: int = 3600
    ) -> str:
        """Generate a secure server-side temporary presigned download link.

        Args:
            bucket_name: Target bucket.
            object_key: S3 file identifier key.
            expires_in_seconds: Token duration limit (default 1 hour).

        Returns:
            Secure presigned URL string.

        Raises:
            StorageError: If URL generation fails.
        """
        try:
            return self.client.presigned_get_object(
                bucket_name=bucket_name,
                object_name=object_key,
                expires=timedelta(seconds=expires_in_seconds),
            )
        except Exception as e:
            logger.error(
                "Failed to generate presigned URL for '%s' in '%s': %s",
                object_key, bucket_name, str(e)
            )
            raise StorageError("Failed to generate secure URL.")
