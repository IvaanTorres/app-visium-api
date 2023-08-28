# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [0.3.0](https://github.com/IvaanTorres/app-visium-api/compare/v0.2.0...v0.3.0) (2023-08-28)


### Features

* **general:** change the welcoming message size preferences ([#21](https://github.com/IvaanTorres/app-visium-api/issues/21)) ([f84a6d5](https://github.com/IvaanTorres/app-visium-api/commit/f84a6d59bc2793efbba019922f6b7cf072672dae))
* **general:** get welcoming message size ([#41](https://github.com/IvaanTorres/app-visium-api/issues/41)) ([da97ad2](https://github.com/IvaanTorres/app-visium-api/commit/da97ad2b43922a1bb41c74595f90eafd3e0f3abf))
* **infos:** get number of login ([#39](https://github.com/IvaanTorres/app-visium-api/issues/39)) ([56bc656](https://github.com/IvaanTorres/app-visium-api/commit/56bc65622201779d7de7483b6cb8b6126b3c11af))
* **locale:** get locale ([#40](https://github.com/IvaanTorres/app-visium-api/issues/40)) ([cab8f02](https://github.com/IvaanTorres/app-visium-api/commit/cab8f02b41919504cd49d74339f2d2c2f83c141a))
* **refresh:** generate new access token ([#25](https://github.com/IvaanTorres/app-visium-api/issues/25)) ([4ce7532](https://github.com/IvaanTorres/app-visium-api/commit/4ce7532d7519b3b3d4b40bbe39a019f206bdac43))
* **settings:** change language preferences ([#20](https://github.com/IvaanTorres/app-visium-api/issues/20)) ([5ddf2ac](https://github.com/IvaanTorres/app-visium-api/commit/5ddf2ac528bf09fa42e354c0a43a3938b5ac19ee))
* **settings:** change username ([#22](https://github.com/IvaanTorres/app-visium-api/issues/22)) ([2480ccf](https://github.com/IvaanTorres/app-visium-api/commit/2480ccfda8239d53063bc64d48a912829032ac6f))


### Style/Clean up

* **arch:** split files in their respective folders ([#47](https://github.com/IvaanTorres/app-visium-api/issues/47)) ([9b522a2](https://github.com/IvaanTorres/app-visium-api/commit/9b522a266b44c1a586d9f22d75d28b69241c9077))
* **function-returns:** arrange the function returns to adapt the object types with the ui ([#45](https://github.com/IvaanTorres/app-visium-api/issues/45)) ([347d050](https://github.com/IvaanTorres/app-visium-api/commit/347d050a3228ff10eaed4313dd3e4cc9a50b5c2f))

## [0.2.0](https://github.com/IvaanTorres/app-visium-api/compare/v0.1.0...v0.2.0) (2023-08-27)


### Features

* **delete-account:** delete users's account ([#23](https://github.com/IvaanTorres/app-visium-api/issues/23)) ([aeee662](https://github.com/IvaanTorres/app-visium-api/commit/aeee662a497392da822c05bf79116c27345705bd))
* **hash:** add salt on hashing ([#16](https://github.com/IvaanTorres/app-visium-api/issues/16)) ([b87d6fe](https://github.com/IvaanTorres/app-visium-api/commit/b87d6fe31e4a4a1ed942c88bf5166e6f249a625b))
* **login:** login user ([#18](https://github.com/IvaanTorres/app-visium-api/issues/18)) ([35f30d7](https://github.com/IvaanTorres/app-visium-api/commit/35f30d74afe2ef6bfd45561a3eac72ce2a0df384))
* **logout:** logout user ([#19](https://github.com/IvaanTorres/app-visium-api/issues/19)) ([f5c0d40](https://github.com/IvaanTorres/app-visium-api/commit/f5c0d401a935c6afc49958da0ba4f84ae3ecb1f4))
* **register:** register new user ([#17](https://github.com/IvaanTorres/app-visium-api/issues/17)) ([8422c79](https://github.com/IvaanTorres/app-visium-api/commit/8422c79e37fbf8a6cb224e3c4fb4625c7d7b4208))
* **security:** create token secrets, password hashing and hmac system based for jwt ([#14](https://github.com/IvaanTorres/app-visium-api/issues/14)) ([af5aaae](https://github.com/IvaanTorres/app-visium-api/commit/af5aaaee67c28ba366670581e78c4b9e706978e3))


### Bug Fixes

* **logout:** get token from authorization and recoke it correctly ([#19](https://github.com/IvaanTorres/app-visium-api/issues/19)) ([c5ef152](https://github.com/IvaanTorres/app-visium-api/commit/c5ef152c1b20b80f7b02b31ef7b2aa6a156dc5d2))

## 0.1.0 (2023-08-24)


### Features

* **boilerplate:** create scaffolding boilerplate ([#1](https://github.com/IvaanTorres/app-visium-api/issues/1)) ([88a371f](https://github.com/IvaanTorres/app-visium-api/commit/88a371f3f9641eb02b08619393542c3e5a806fb2))
* **migrations:** create migrations ([#11](https://github.com/IvaanTorres/app-visium-api/issues/11)) ([c6fa1e1](https://github.com/IvaanTorres/app-visium-api/commit/c6fa1e13e6e2d07ddea0e3912bcc55e863989289))


### Build

* **deps:** install external dependencies API ([#2](https://github.com/IvaanTorres/app-visium-api/issues/2)) ([17f07be](https://github.com/IvaanTorres/app-visium-api/commit/17f07be98f63a86883cc822d04b0ce4e9282027e))
* **docker:** dockerize the app API ([#5](https://github.com/IvaanTorres/app-visium-api/issues/5)) ([24300a3](https://github.com/IvaanTorres/app-visium-api/commit/24300a371c74651e7840b40d2340b96152a2cea8))
* **husky:** install and set up husky API ([#3](https://github.com/IvaanTorres/app-visium-api/issues/3)) ([37ad3db](https://github.com/IvaanTorres/app-visium-api/commit/37ad3db36fdc1655f5d8404fa24cebdca79e9b9a))
* **standard-version:** install and set up standard-version API ([#4](https://github.com/IvaanTorres/app-visium-api/issues/4)) ([137a183](https://github.com/IvaanTorres/app-visium-api/commit/137a183be9fd687aa0a665652747203b18a8509f))
