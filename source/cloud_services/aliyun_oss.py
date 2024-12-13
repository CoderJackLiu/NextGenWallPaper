import oss2


class AliyunOSS:
    def __init__(self, access_key_id, access_key_secret, endpoint, bucket_name):
        if not all([access_key_id, access_key_secret, endpoint, bucket_name]):
            print("OSS configuration is incomplete. OSS functionality is disabled.")
            self.enabled = False
            return

        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)
        self.enabled = True  # 标记 OSS 功能已启用

    def list_wallpapers(self, prefix=""):
        if not self.enabled:
            raise ValueError("OSS functionality is disabled due to incomplete configuration.")
        wallpapers = []
        for obj in oss2.ObjectIterator(self.bucket, prefix=prefix):
            if obj.key.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                wallpapers.append(obj.key)
        return wallpapers

    def download_wallpaper(self, remote_file, local_path):
        if not self.enabled:
            raise ValueError("OSS functionality is disabled due to incomplete configuration.")
        self.bucket.get_object_to_file(remote_file, local_path)
