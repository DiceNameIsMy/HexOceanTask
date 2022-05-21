from abc import ABC, abstractmethod

import boto3

from django.conf import settings


class AbstractExpiringLinkClient(ABC):
    @abstractmethod
    def __init__(self, access_key_id: str, secret_access_key: str, bucket_name: str) -> None:
        pass

    @abstractmethod
    def create_link(self, url: str, exp: int):
        pass


class S3ExpiringLinkClient(AbstractExpiringLinkClient):
    def __init__(self, access_key_id: str, secret_access_key: str, bucket_name: str) -> None:
        self.bucket_name = bucket_name
        self.session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        )
        self.bucket_region_name = self._get_region_name(self.session, self.bucket_name)
        self.client = self.session.client(
            "s3",
            region_name=self.bucket_region_name,
            config=boto3.session.Config(signature_version="s3v4"),
        )

    def create_link(self, url: str, exp: int) -> str:
        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket_name, "Key": url},
            ExpiresIn=exp,
        )

    def _get_region_name(self, session: boto3.Session, bucket_name: str) -> str:
        return session.client("s3").get_bucket_location(Bucket=bucket_name)["LocationConstraint"]


class FakeExpiringLinkClient(AbstractExpiringLinkClient):
    def __init__(self, access_key_id: str, secret_access_key: str, bucket_name: str) -> None:
        pass

    def create_link(self, url: str, exp: int) -> str:
        return f"http://localhost:8000/{url}"


if settings.USE_AWS_S3_FOR_FILE_STORAGE:
    expiring_link_client_class = S3ExpiringLinkClient
else:
    expiring_link_client_class = FakeExpiringLinkClient

s3_expiring_link_client: AbstractExpiringLinkClient = expiring_link_client_class(
    access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
    secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
    bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
)
