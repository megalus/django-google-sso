# CHANGELOG


## v8.0.0 (2024-10-09)

### Breaking

* ci!: bump version

BREAKING CHANGE commit ([`4cef07a`](https://github.com/megalus/django-google-sso/commit/4cef07acf3f659d166ac3bccfd92c0a7ce4404bb))

### Documentation

* docs: update docs.

Closes #41 ([`6b5da42`](https://github.com/megalus/django-google-sso/commit/6b5da421d6b412c4b8abcd9741e43943ff30c6e2))

* docs: update docs ([`9393cbb`](https://github.com/megalus/django-google-sso/commit/9393cbb7cf955828c6b6252e9c0677f8316af749))

* docs: update docs ([`d1de7d5`](https://github.com/megalus/django-google-sso/commit/d1de7d5d3444b70a6bdd884a432ebc99327fd3a8))

### Unknown

* Add support to 3.13 (#47)

* Allow "*" in GOOGLE_SSO_ALLOWABLE_DOMAINS

* feat!: Add support to Python to 3.13 and remove 3.10

This is a BREAKING CHANGE commit

* chore: fix unit tests

* chore: fix line breaks

* chore: fix github actions

---------

Co-authored-by: Pavel Mises <id@dqd.cz> ([`0e6b547`](https://github.com/megalus/django-google-sso/commit/0e6b5474b1decfe3fba4bf6e903f4f60f05ea80c))


## v7.1.0 (2024-09-17)

### Features

* feat: Add new option GOOGLE_SSO_SHOW_FAILED_LOGIN_MESSAGE

Also failed attempts to create user in database will be logged on terminal ([`e53accb`](https://github.com/megalus/django-google-sso/commit/e53accba4b3bb9046bbeb68aa26f23d345091c38))


## v7.0.0 (2024-08-29)

### Breaking

* feat!: Remove support for Django 4.1 and add support to 5.1

This is a BREAKING CHANGE commit. ([`6e7573a`](https://github.com/megalus/django-google-sso/commit/6e7573a0acee58e9bdcd13ac60c389435dc314ba))

### Documentation

* docs: small fixes ([`5219a90`](https://github.com/megalus/django-google-sso/commit/5219a90717f3700c93b116b4285260d9a8a0e5d4))


## v6.5.0 (2024-08-29)

### Documentation

* docs: update settings.md ([`d0f3073`](https://github.com/megalus/django-google-sso/commit/d0f3073dae2117ccd935f4083a3decf039a85db1))

### Features

* feat: add `GOOGLE_SSO_PRE_VALIDATE_CALLBACK` option.

Fixes #43 ([`8163b93`](https://github.com/megalus/django-google-sso/commit/8163b93cf8950a255daaea764c87d1c98237eab4))


## v6.4.0 (2024-08-13)

### Documentation

* docs: update settings.md with current logo path ([`fa85eb8`](https://github.com/megalus/django-google-sso/commit/fa85eb8edd2f58959d291a06acf40326aa80a5e1))

* docs: update Django version numbers to match implementation ([`a732f9d`](https://github.com/megalus/django-google-sso/commit/a732f9dc97794699249d3ab944d6e36b8a633f75))

### Features

* feat: add new option GOOGLE_SSO_SAVE_BASIC_GOOGLE_INFO.

When set to False, the GoogleSSOUser model will not be created or updated for the logged user. Default is True.

Fixes #39 ([`6a5a4d4`](https://github.com/megalus/django-google-sso/commit/6a5a4d4d90ab953c25b52058a4466702e59e65a6))

### Unknown

* Merge pull request #40 from paulschreiber/main

docs: update settings.md with current logo path ([`177782d`](https://github.com/megalus/django-google-sso/commit/177782d05bedf1ffd5ff53724f909d1e0b1c9258))

* Merge pull request #42 from paulschreiber/fix/docs

docs: update Django version numbers to match implementation ([`27e13dc`](https://github.com/megalus/django-google-sso/commit/27e13dc9cc2ecf98afe3888117aabe051965a750))


## v6.3.0 (2024-07-31)

### Features

* feat: add option to add all created users as staff

Also fix bugs when reading upper and lower case emails ([`1a7b3ab`](https://github.com/megalus/django-google-sso/commit/1a7b3abc787126679db2bcc005ed45aac16381a9))


## v6.2.1 (2024-06-07)

### Fixes

* fix: Add support to Django USERNAME_FIELD ([`b62f560`](https://github.com/megalus/django-google-sso/commit/b62f560255b4662c2816b9d8b5a3b6b12eb73762))

### Unknown

* Merge pull request #36 from megalus/develop

develop ([`13984de`](https://github.com/megalus/django-google-sso/commit/13984dea3e550fe96e9de05ef6d501f18f46c4ae))

* Merge pull request #35 from AndrewGrossman/main

Handle user model w/o username field ([`2663dcb`](https://github.com/megalus/django-google-sso/commit/2663dcb93252b78605cab7b0f0367a1d281049eb))

* Handle user model w/o username field

Encountered this in a project based upon Django Cookie Cutter, where the
username field is not present. This change avoids trying to pass
"username" as a default to the user creation if it is not present,
avoiding the error that would otherwise result. ([`c0cb6a5`](https://github.com/megalus/django-google-sso/commit/c0cb6a58d23165764beb86c10f374ec539b8d910))


## v6.2.0 (2024-04-23)

### Features

* feat: add more control on messaging

Use the `GOOGLE_SSO_ENABLE_LOGS` to enable/disable logs. Logs now will show all info send to django messages.

Use the `GOOGLE_SSO_ENABLE_MESSAGES` to enable/disable django messages. ([`c718030`](https://github.com/megalus/django-google-sso/commit/c7180305e05b6d146e6369e4635cebee9de17a57))


## v6.1.1 (2024-04-09)

### Fixes

* fix: add token in request before call pre-create callback ([`2bf6467`](https://github.com/megalus/django-google-sso/commit/2bf6467c948ded6fc98df1e0d07ec84d4a9ffa0c))


## v6.1.0 (2024-04-09)

### Features

* feat: Add support to custom attributes in User model before creation.

Use the `GOOGLE_SSO_PRE_CREATE_CALLBACK` to define a custom function which can return a dictionary which will be used during user creation for the `defaults` value. ([`cc9ad6a`](https://github.com/megalus/django-google-sso/commit/cc9ad6a6dc5263f6c9efd139102bd9070962d97a))


## v6.0.2 (2024-03-14)

### Continuous Integration

* ci: add stale bot for github ([`e4f457e`](https://github.com/megalus/django-google-sso/commit/e4f457e1efcf129ddd7be70bff39572daab605e5))

### Fixes

* fix: error when field `locale` was not available on Google API response.

If you need to define a default value for this field, please use the `GOOGLE_SSO_DEFAULT_LOCALE` option.

Also make these fields optional: `given_name`, `given_name` and `picture`

Resolves #31 ([`646d986`](https://github.com/megalus/django-google-sso/commit/646d986d609aba7acc4f0df0ea0f6136a4fe7747))

### Unknown

* Merge pull request #32 from megalus/develop

Fix missing field locale in Google Response ([`05a3383`](https://github.com/megalus/django-google-sso/commit/05a33838bfe6f4e3febd83d9b75d54fc824e2d8b))


## v6.0.1 (2024-03-12)

### Chores

* chore: Refactor UserHelper ([`acdf98d`](https://github.com/megalus/django-google-sso/commit/acdf98dee95285afe4aa02c38d53379e47098666))

### Fixes

* fix: Bump version ([`59907fd`](https://github.com/megalus/django-google-sso/commit/59907fdb0234e73ffb498b7af5ebce3e36055c94))

### Unknown

* Merge pull request #30 from megalus/develop

New Release ([`c95154d`](https://github.com/megalus/django-google-sso/commit/c95154d8b13bd5fb227f323ad7fa1565beea4148))

* Merge pull request #29 from Anexen/fix/empty-username

Fix an issue with empty username when user creation disrupted ([`2830f8c`](https://github.com/megalus/django-google-sso/commit/2830f8c18a290a5487611a1710452ea73db56636))

* fix an issue with empty username when user creation failed ([`6f1121e`](https://github.com/megalus/django-google-sso/commit/6f1121e5164b5bd3557ded6c66a10a79ec8565e0))


## v6.0.0 (2024-03-12)

### Breaking

* feat!: Add basic support to custom login templates.

Rework the login.html and login_sso.html to simplify login template customization. The use case is the [Django Unfold](https://github.com/unfoldadmin/django-unfold) package. This is a BREAKING CHANGE for the static and html files.

Also:
* Remove pytest-lazy-fixture to upgrade pytest to latest version ([`75d979f`](https://github.com/megalus/django-google-sso/commit/75d979f2999dc77665aeb6cec64bd2c9c8a7c16d))

### Documentation

* docs: Better Stela use.

Also add missing tests in GitHub Actions ([`f34152f`](https://github.com/megalus/django-google-sso/commit/f34152ffde5a9eb1eb31a3983e1eba6e840838a0))


## v5.0.0 (2023-12-20)

### Breaking

* feat!: New version

BREAKING CHANGE:
* Remove Django 4.1 support
* Add Django 5.0 support
* Fix `SSO_USE_ALTERNATE_W003` bug
* Fix several CSS issues with custom logo images
* Update docs ([`dc3560c`](https://github.com/megalus/django-google-sso/commit/dc3560c12398037f289dc1e8b08d4c8d40b7577a))


## v4.0.0 (2023-11-23)

### Breaking

* feat!: v4.0

BREAKING CHANGE: New changes:

* Drop Python 3.9 support
* Add Python 3.12 support
* Add compatibility with multiple django-sso packages (ie. django-microsoft-sso)
* Renamed option GOOGLE_SSO_SHOW_FORM_ON_ADMIN_PAGE to SSO_SHOW_FORM_ON_ADMIN_PAGE
* Fix default google icon logo 404 error ([`7212d2c`](https://github.com/megalus/django-google-sso/commit/7212d2c30a25710a507ed26e5640284bd8e87486))

### Unknown

* Revert "ci: fix permission in actions"

This reverts commit bad8be733943f4a2bc03f07f74736f9b824993e9. ([`22f87bc`](https://github.com/megalus/django-google-sso/commit/22f87bcfd56d4a2158da45ccef8c459e0e619a80))


## v3.3.0 (2023-09-27)

### Continuous Integration

* ci: fix permission in actions ([`bad8be7`](https://github.com/megalus/django-google-sso/commit/bad8be733943f4a2bc03f07f74736f9b824993e9))

* ci: add permissions ([`3189773`](https://github.com/megalus/django-google-sso/commit/31897733fe3bda39fe2f011d1d941d50d632d563))

### Documentation

* docs: update example in docs ([`0db95f8`](https://github.com/megalus/django-google-sso/commit/0db95f8388329fc7937b1e10299c74fb7ba2960a))

* docs: better docs ([`2b3e3cb`](https://github.com/megalus/django-google-sso/commit/2b3e3cb3e72a9e6f4ec2b3a03660439b8a83139d))

### Features

* feat: Add GOOGLE_SSO_SHOW_FORM_ON_ADMIN_PAGE option.

This commit adds the missing logic and documentation for this new option. ([`efc33cd`](https://github.com/megalus/django-google-sso/commit/efc33cd418e3a89044687c40788d195abc4a38a8))

### Unknown

* Merge pull request #27 from megalus/develop

v3.3 ([`2d79094`](https://github.com/megalus/django-google-sso/commit/2d79094c1472f72ecd9c8c86bdb1e6251970f972))

* Merge pull request #26 from jnoring/optionally-hide-login

Optionally hide the login boxes on the admin page ([`76cde44`](https://github.com/megalus/django-google-sso/commit/76cde44d0cfaf8c10badc95063412d543a8bcff3))

* Optionally hide the login boxes on the admin page

For my site, I want to manage access to google admin _only_ through
SSO; I don't even want to expose the login boxes to anyone navigating
to the admin site. Add an optional setting to hide the standard
login (defaults to "show" for backwards compatibility) ([`734bf45`](https://github.com/megalus/django-google-sso/commit/734bf45d517c1f490ca8d357a2d5799f520921dd))


## v3.2.0 (2023-09-19)

### Documentation

* docs: update example code in admin.md ([`4c38551`](https://github.com/megalus/django-google-sso/commit/4c38551647b45ff55872929230ac8c8697bab137))

### Features

* feat: Add GOOGLE_SSO_ALWAYS_UPDATE_USER_DATA option

* Add logic help use Google as Single Source of Truth (thanks @ckoppelman)

The update introduces token handling for Google users within the session and implements Pre-Login Callback functionality within the example app's backend. This allows for execution of custom code post-user authentication, including updating user information using Google user token. This enhances customizability and user information update capabilities. The example code and documentation have been updated accordingly.

Resolves #23 ([`a106fcf`](https://github.com/megalus/django-google-sso/commit/a106fcf166b1463ddf159112ffa0d43ee999868f))

### Unknown

* Merge pull request #25 from megalus/develop

v 3.2 ([`ee64dc6`](https://github.com/megalus/django-google-sso/commit/ee64dc61ee83e034124fbcd346c05124fb8f634e))

* Merge pull request #24 from ckoppelman/always-update-user-data

Always update user data ([`fdfcaa8`](https://github.com/megalus/django-google-sso/commit/fdfcaa8a26b74f4ed59d09ba8dbfbbfea4575495))

* Create setting to always update user data from Google on login. ([`6a80fe2`](https://github.com/megalus/django-google-sso/commit/6a80fe20b0a59f8da179acd61c5c420edeb44868))

* Exclude .venv and site-packages from pre-commit hooks to allow commits ([`84f2b7a`](https://github.com/megalus/django-google-sso/commit/84f2b7a24f62cbc571f9a088c4d05a9508dc1e86))


## v3.1.0 (2023-08-16)

### Features

* feat: Add option to save access token

This commit introduces functionality to save the Google SSO access token to the user's session via a new configuration parameter (`GOOGLE_SSO_SAVE_ACCESS_TOKEN`), providing finer control over logout functionality. Default value for this parameter is `False`. ([`cd23c76`](https://github.com/megalus/django-google-sso/commit/cd23c76010a589e0bbe56e4bbab673668394e378))

* feat: Add new configuration parameters and fix bugs

* Add configuration GOOGLE_SSO_LOGIN_FAILED_URL to finetune redirection after login failed. Thanks @simook
* Add configuration GOOGLE_SSO_NEXT_URL to finetune redirection after login succeeds. Thanks @simook
* Fix error when adding Google SSO inline to User Admin. Thanks @jnoring
* Update Github Actions ([`3b26037`](https://github.com/megalus/django-google-sso/commit/3b26037c1ebe549d10b4a25533d5ed72ad4e4c99))

### Unknown

* Merge pull request #21 from megalus/develop

Version 3.1 ([`0ab66ac`](https://github.com/megalus/django-google-sso/commit/0ab66acf2a43fdd1f2a40fd9300b602388a24bcd))

* Merge pull request #20 from simook/main

Fixed a TypeError and added a configuration parameter. ([`8abd39f`](https://github.com/megalus/django-google-sso/commit/8abd39f1d5ff07026859ccf25cf664e0b05a7377))

* Added a configuration parameter that defines the URL used in the callback method. ([`f9d9f8b`](https://github.com/megalus/django-google-sso/commit/f9d9f8b3ec6cc94753057f0a75778c0f44d0d116))

* Fixed a TypeError when the next query param is absent. ([`b6fed53`](https://github.com/megalus/django-google-sso/commit/b6fed534db87765465cce81df7e299502b97cf1b))

* Merge pull request #19 from jnoring/patch-1

Update admin.py ([`62c8b27`](https://github.com/megalus/django-google-sso/commit/62c8b27feccdd31691d5898884b63829be40c427))

* Update admin.py

This needs to ultimately be a list or a tuple--not a set. ([`eb79550`](https://github.com/megalus/django-google-sso/commit/eb7955033fd43ce48d7cdcc7e3bed439e17cf8d3))


## v3.0.0 (2023-04-19)

### Breaking

* feat!: version 3.0

BREAKING CHANGE:

* Drop support to Django 3.2
* Rework code to make compatible with future login projects
* Add fully customizable button ([`24bfb2e`](https://github.com/megalus/django-google-sso/commit/24bfb2e5849f3a637de68193506c3a943fcdbba7))

### Chores

* chore: fix unit tests ([`f3d7d92`](https://github.com/megalus/django-google-sso/commit/f3d7d92bff9a67184a02b9b7b1bdbaff15389d08))

* chore: fix example images ([`617eb77`](https://github.com/megalus/django-google-sso/commit/617eb778e6b253d1d642fe50c9b4b1609706a428))

* chore: add missing image and fix pycharm scripts ([`2fe5c17`](https://github.com/megalus/django-google-sso/commit/2fe5c1776988a9a5956549edb37516c05dad06cc))

### Documentation

* docs: fix typo ([`08c782d`](https://github.com/megalus/django-google-sso/commit/08c782df65519afac67d4662f568b3b3841b26c2))

* docs: update docs ([`a2ef5b7`](https://github.com/megalus/django-google-sso/commit/a2ef5b7026a84e971b6a1b1bf3544e53c7bf60e5))

### Unknown

* Merge pull request #16 from megalus/develop

Version 3.0 ([`cdc38ab`](https://github.com/megalus/django-google-sso/commit/cdc38ab07a99780bf08e1298c70e8ba12340fa40))

* Merge pull request #15 from jhhayashi/jhh/user-admin-monkeypatch

Use the existing UserAdmin model if it's already registered ([`6aece66`](https://github.com/megalus/django-google-sso/commit/6aece668a184f964d42e737a5bb25d5dc261164f))

* Use the existing UserAdmin model if it's already registered ([`dc6bbfa`](https://github.com/megalus/django-google-sso/commit/dc6bbfa39cacbc5ad7baf99691a5f59d3a4e46e2))


## v2.5.0 (2023-04-05)

### Chores

* chore: add missing Optional ([`a80cd75`](https://github.com/megalus/django-google-sso/commit/a80cd75716375ffd713e7bd9ffaab9225df1535e))

### Continuous Integration

* ci: add .env ([`f2582a5`](https://github.com/megalus/django-google-sso/commit/f2582a58dc59f222397169a03e6d49aacfba51f6))

* ci: persist credentials ([`a8364ea`](https://github.com/megalus/django-google-sso/commit/a8364ea3676a59e795e0ba286eff2868fd8c15d3))

* ci: fix action version ([`46d3d6c`](https://github.com/megalus/django-google-sso/commit/46d3d6cae8091ea6423d75194b2dd98e489a1649))

* ci: move repository to megalus organization

Resolves DGS-2 ([`dfeaa54`](https://github.com/megalus/django-google-sso/commit/dfeaa547fc1abd5f276cd37513a9ea874c12699c))

### Documentation

* docs: update Stela example ([`6ff6676`](https://github.com/megalus/django-google-sso/commit/6ff6676b04729ef8d2687ee7f54bd31e68cba3a0))

* docs: improve documentation ([`131f1b1`](https://github.com/megalus/django-google-sso/commit/131f1b10a1398cc17a8eec95feb571de3cf6a0c8))

### Features

* feat: Update to Django 4.2

This is a BREAKING CHANGE: drop support to python 3.8

* Update documentation
* Remove Python 3.8

Resolves DGS-4 ([`677a5da`](https://github.com/megalus/django-google-sso/commit/677a5da8c4d0815595e4aaa72c363f8feb409a93))

### Unknown

* Merge pull request #14 from megalus/feat/DGS-4

Add Django 4.2 ([`96568a9`](https://github.com/megalus/django-google-sso/commit/96568a905a2ddc9936a7649a40fa91d8a086a7ed))


## v2.4.1 (2023-02-25)

### Continuous Integration

* ci: github action update ([`7504bbc`](https://github.com/megalus/django-google-sso/commit/7504bbcb18dea18e5b10486b3f103c9edc845dca))

### Fixes

* fix: UserManager error when GOOGLE_SSO_AUTO_CREATE_USERS is set to False ([`4451c6b`](https://github.com/megalus/django-google-sso/commit/4451c6bf228e29cba14b11fd6ee17d9f2089cefd))

* fix(docs/how.md): add missing S with GOOGLE_SSO_AUTO_CREATE_USERS ([`3e9b661`](https://github.com/megalus/django-google-sso/commit/3e9b661eaec4693541b92f85de65129f18bc3fe2))

### Unknown

* Merge pull request #13 from chrismaille/develop

Fix GOOGLE_SSO_AUTO_CREATE_USERS issues ([`9d54638`](https://github.com/megalus/django-google-sso/commit/9d546380d408a3aef652a37afae6dbac6bbf1618))

* Merge pull request #11 from blueyed/doc-typo

fix(docs/how.md): add missing S with GOOGLE_SSO_AUTO_CREATE_USERS ([`72f08b7`](https://github.com/megalus/django-google-sso/commit/72f08b75197ed4af0cdcde5026be113c1a0c005c))


## v2.4.0 (2023-01-23)

### Features

* feat: Add GOOGLE_SSO_PRE_LOGIN_CALLBACK feature

Resolves #10 ([`44ade37`](https://github.com/megalus/django-google-sso/commit/44ade37ce4f65a530562da4edbdc4c5d122d9f85))


## v2.3.1 (2023-01-18)

### Fixes

* fix: small fixes

* typo in environments variables (thanks @ciodaro)
* update github action dependencies ([`1ec44cc`](https://github.com/megalus/django-google-sso/commit/1ec44cc5f6080e8de67a0548b3af647ba96cc262))

### Unknown

* Merge pull request #9 from ciodaro/fix/settings-var-name

Fixing settings var name from GOGGLE to GOOGLE ([`285ed2b`](https://github.com/megalus/django-google-sso/commit/285ed2b6e18540c5b3fc1b1d464e7890b3fbdc1c))

* Fixing settings var name from GOGGLE to GOOGLE ([`7424d1b`](https://github.com/megalus/django-google-sso/commit/7424d1be12f91893ae5cff88bed5a174a2990f4c))


## v2.3.0 (2022-10-28)

### Chores

* chore: fix python version in actions ([`aa73aa4`](https://github.com/megalus/django-google-sso/commit/aa73aa4e4d5e7265fef695d402860300725cf1c2))

* chore: fix docs ([`9a8f841`](https://github.com/megalus/django-google-sso/commit/9a8f841d4f18dcbe4914961cf800eaca103e1e2a))

### Continuous Integration

* ci: fix poetry add command ([`606fe69`](https://github.com/megalus/django-google-sso/commit/606fe699355ae543bea39183d8d4f77f4d7d8534))

* ci: force min version for click ([`0438b1a`](https://github.com/megalus/django-google-sso/commit/0438b1aa59221ec8fcb4cc73b544cbc57a787475))

* ci: fix correct numbers ([`6e4ceaf`](https://github.com/megalus/django-google-sso/commit/6e4ceafb6e275bb1b7fc639753b45a668a655cf4))

* ci: update github actions versions ([`751fe5b`](https://github.com/megalus/django-google-sso/commit/751fe5b95cae2138ee347f45596739e3d97e2e71))

### Features

* feat: release 2.3.0

### New features

* Add Python 3.11 support
* Add Django 4.1 support

### New settings options:

* GOOGLE_SSO_AUTHENTICATION_BACKEND: set up a custom authentication backend to log in the Google SSO users. Thanks @savionak. Resolves #4
* GOOGLE_SSO_AUTO_CREATE_USERS: toggle auto-create users

### New documentation:

Full documentation is now hosted on https://chrismaille.github.io/django-google-sso/

### Fix bugs

* Fix error when anonymous request session is not created. Resolves #3
* Fix error when Google Picture URL is larger than 255 characters. We accept up to 2,000 characters now. Resolves #6 ([`8ef3b04`](https://github.com/megalus/django-google-sso/commit/8ef3b04e2c096338c4b92126ebbf4f6cfac0d208))

* feat: Add new settings option GOOGLE_SSO_AUTHENTICATION_BACKEND

Use this option if you have multiple authentication backends to select one. ([`4212782`](https://github.com/megalus/django-google-sso/commit/4212782eae4c1400e1d9634b79df83f4a5d36f3d))

### Unknown

* Merge pull request #8 from chrismaille/develop

New Release 2.3.0 ([`85571ba`](https://github.com/megalus/django-google-sso/commit/85571ba22fd90bcb10dd6ac43285696b430e5f8c))

* Merge pull request #7 from chrismaille/update_python_version

New release ([`81612e5`](https://github.com/megalus/django-google-sso/commit/81612e559b59331211f39e1862637be238cd3358))

* Merge pull request #5 from savionak/multiple-backend-fix

feat: Add new settings option GOOGLE_SSO_AUTHENTICATION_BACKEND ([`125012b`](https://github.com/megalus/django-google-sso/commit/125012b9bea7c3b774a34728f57b76afb18c90c2))

* Create FUNDING.yml ([`5b6f2f6`](https://github.com/megalus/django-google-sso/commit/5b6f2f6c6ae944a9361f0ec6314267f9101ed2d1))


## v2.2.0 (2022-09-06)

### Features

* feat: Make Sites Framework optional

To define the callback netloc, you can simply use the GOOGLE_SSO_CALLBACK_DOMAIN settings. Please make not if you use both, the value on GOOGLE_SSO_CALLBACK_DOMAIN will prevail. ([`e5a3839`](https://github.com/megalus/django-google-sso/commit/e5a38395b68ca4614b67cc5868c5adfd2a504f82))


## v2.1.0 (2022-09-02)

### Features

* feat: Add new settings option GOOGLE_SSO_CALLBACK_DOMAIN

Use this option if you can't or don't want to use Django Sites Framework to determine which domain will be used to generate Django SSO Callback URL.

For example, if you set `GOOGLE_SSO_CALLBACK_DOMAIN="my-other-domain.com"`, you callback url will be `https://my-other-domain.com/google_sso/callback/` ([`4b49059`](https://github.com/megalus/django-google-sso/commit/4b490596a0e2efc47f3067628bb939d832da5ae5))


## v2.0.0 (2022-02-23)

### Breaking

* feat: Add django 4 support

BREAKING CHANGE: update tests and example app ([`dcb5f9f`](https://github.com/megalus/django-google-sso/commit/dcb5f9ff2329e54f38985cfb2eb1c0edd06ebf5a))

### Unknown

* Merge pull request #1 from chrismaille/2.0

Version 2.0 ([`11639a8`](https://github.com/megalus/django-google-sso/commit/11639a8a8766e7ecb6d1124389dc9a2a6fcc2694))


## v1.0.2 (2022-02-23)

### Continuous Integration

* ci: update actions logic ([`94d8947`](https://github.com/megalus/django-google-sso/commit/94d8947b7105059cc871ae52fe3fd5c1a8149b1b))

### Fixes

* fix: change license to MIT ([`750f979`](https://github.com/megalus/django-google-sso/commit/750f9791dcc7057359da08b69774515b63a3578d))


## v1.0.1 (2021-11-23)

### Documentation

* docs: Add `login_required` use example and add Django Classifiers ([`fccc7b6`](https://github.com/megalus/django-google-sso/commit/fccc7b62174a2898e93a0ad483ffe014884b538c))

* docs: Update README.md ([`c2e6c3b`](https://github.com/megalus/django-google-sso/commit/c2e6c3b17388f9ac7d5442f3d780cc2859071afd))

### Fixes

* fix: Update Django Classifiers ([`17664cb`](https://github.com/megalus/django-google-sso/commit/17664cb89430f2be730b859a3d5926acb708300c))


## v1.0.0 (2021-11-22)

### Breaking

* feat!: First Release

BREAKING CHANGE: This is version 1.0. To find additional information please check README.md file. ([`54d979f`](https://github.com/megalus/django-google-sso/commit/54d979f06c76f6985483d642823f85c006776b19))


## v0.2.1 (2021-11-20)

### Continuous Integration

* ci: fix bad reverse url at import module level ([`50fc39f`](https://github.com/megalus/django-google-sso/commit/50fc39f2a7223b2100a8d381e08ecbf496d008d1))

* ci: add missing pytest lib ([`afed6d5`](https://github.com/megalus/django-google-sso/commit/afed6d526b6ee7cbbed01fe074d314726577f887))

* ci: update poetry version ([`7252ef6`](https://github.com/megalus/django-google-sso/commit/7252ef65c8b6947e704821732e9ca08c26ca631a))

* ci: fix test versions ([`22544f3`](https://github.com/megalus/django-google-sso/commit/22544f30dca4c7f382ab41ad53d531e801a99c41))

### Features

* feat: Add alpha version ([`98c78e5`](https://github.com/megalus/django-google-sso/commit/98c78e589016948f352c67849e36d937c455456e))

### Fixes

* fix: unit test ([`220920c`](https://github.com/megalus/django-google-sso/commit/220920cef5913bd24e78fe4da379b66b037078df))
