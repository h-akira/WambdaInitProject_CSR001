from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
  username = StringField('Username', [
    validators.Length(min=1, max=63),
    validators.DataRequired()
  ])
  password = PasswordField('Password', [
    validators.Length(min=8, max=63),
    validators.DataRequired()
  ])

class SignupForm(Form):
  username = StringField('Username', [
    validators.Length(min=1, max=63),
    validators.DataRequired()
  ])
  email = StringField('Email', [
    validators.Length(min=1, max=63),
    validators.DataRequired()
  ])
  password = PasswordField('Password', [
    validators.Length(min=8, max=63),
    validators.DataRequired()
  ])
  confirm_password = PasswordField('Confirm Password', [
    validators.Length(min=8, max=63),
    validators.DataRequired()
  ])

  def validate(self):
    if not super().validate():
      return False

    if self.password.data != self.confirm_password.data:
      self.confirm_password.errors.append('パスワードが一致しません')
      return False

    return True

class VerifyForm(Form):
  username = StringField(
    validators=[DataRequired(), Length(min=1, max=63)],
    label='ユーザー名'
  )
  code = StringField(
    validators=[DataRequired(), Length(min=6, max=6)],
    label='確認コード'
  )

class ChangePasswordForm(Form):
  current_password = PasswordField(
    validators=[DataRequired(), Length(min=8, max=63)],
    label='現在のパスワード'
  )
  new_password = PasswordField(
    validators=[DataRequired(), Length(min=8, max=63)],
    label='新しいパスワード'
  )
  confirm_password = PasswordField(
    validators=[DataRequired(), Length(min=8, max=63)],
    label='新しいパスワード（確認）'
  )

  def validate(self):
    if not super().validate():
      return False

    if self.new_password.data != self.confirm_password.data:
      self.confirm_password.errors.append('パスワードが一致しません')
      return False

    return True

class ForgotPasswordForm(Form):
  username = StringField(
    validators=[DataRequired(), Length(min=1, max=63)],
    label='ユーザー名'
  )

class ResetPasswordForm(Form):
  username = StringField(
    validators=[DataRequired(), Length(min=1, max=63)],
    label='ユーザー名'
  )
  confirmation_code = StringField(
    validators=[DataRequired(), Length(min=6, max=6)],
    label='確認コード'
  )
  new_password = PasswordField(
    validators=[DataRequired(), Length(min=8, max=63)],
    label='新しいパスワード'
  )
  confirm_password = PasswordField(
    validators=[DataRequired(), Length(min=8, max=63)],
    label='新しいパスワード（確認）'
  )

  def validate(self):
    if not super().validate():
      return False

    if self.new_password.data != self.confirm_password.data:
      self.confirm_password.errors.append('パスワードが一致しません')
      return False

    return True

class DeleteAccountForm(Form):
  current_password = PasswordField(
    validators=[DataRequired(), Length(min=8, max=63)],
    label='現在のパスワード'
  )
  confirmation = StringField(
    validators=[DataRequired()],
    label='削除の確認'
  )

  def validate(self):
    if not super().validate():
      return False

    if self.confirmation.data != 'DELETE':
      self.confirmation.errors.append('削除を確認するため「DELETE」と入力してください')
      return False

    return True