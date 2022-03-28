import base64
import datetime
import hashlib
import math
import secrets
from decimal import Decimal

_PROTECTED_TYPES = (
    type(None),
    int,
    float,
    Decimal,
    datetime.datetime,
    datetime.date,
    datetime.time,
)

RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


class DjangoPBKDF2PasswordHasher:
    """
    Ported this from django so that we can validate existing paswords created in/with
    the django framework.
    """

    algorithm = "pbkdf2_sha256"
    iterations = 100000
    digest = hashlib.sha256

    def encode(self, password, salt, iterations=None):
        assert password is not None
        assert salt and "$" not in salt
        if not iterations:
            iterations = self.iterations
        hash = self.pbkdf2(password, salt, iterations, digest=self.digest)
        hash = base64.b64encode(hash).decode("ascii").strip()
        return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)

    def verify(self, password, encoded):
        algorithm, iterations, salt, hash = encoded.split("$", 3)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, salt, int(iterations))
        return self.constant_time_compare(encoded, encoded_2)

    def pbkdf2(self, password, salt, iterations, dklen=0, digest=None):
        """Return the hash of password using pbkdf2."""
        if digest is None:
            digest = hashlib.sha256
        dklen = dklen or None
        password = self.force_bytes(password)
        salt = self.force_bytes(salt)
        return hashlib.pbkdf2_hmac(digest().name, password, salt, iterations, dklen)

    def force_bytes(self, s, encoding="utf-8", strings_only=False, errors="strict"):
        # Handle the common case first for performance reasons.
        if isinstance(s, bytes):
            if encoding == "utf-8":
                return s
            else:
                return s.decode("utf-8", errors).encode(encoding, errors)
        if strings_only and self.is_protected_type(s):
            return s
        if isinstance(s, memoryview):
            return bytes(s)
        return str(s).encode(encoding, errors)

    def is_protected_type(self, obj):
        return isinstance(obj, _PROTECTED_TYPES)

    def constant_time_compare(self, val1, val2):
        """Return True if the two strings are equal, False otherwise."""
        return secrets.compare_digest(self.force_bytes(val1), self.force_bytes(val2))

    def salt(self):
        char_count = math.ceil(self.salt_entropy / math.log2(len(RANDOM_STRING_CHARS)))
        return self.get_random_string(char_count, allowed_chars=RANDOM_STRING_CHARS)

    def get_random_string(self, length, allowed_chars=RANDOM_STRING_CHARS):
        return "".join(secrets.choice(allowed_chars) for i in range(length))


hasher = DjangoPBKDF2PasswordHasher()
