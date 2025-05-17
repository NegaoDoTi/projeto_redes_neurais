from itsdangerous import URLSafeSerializer
from config.config import SECRET_KEY

serializer = URLSafeSerializer(SECRET_KEY)