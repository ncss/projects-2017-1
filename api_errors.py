class UserExistsError(Exception):
  def __init__(self, message):
      super().__init__(message)

class BucketNotFoundError(Exception):
  def __init__(self, message):
      super().__init__(message)
