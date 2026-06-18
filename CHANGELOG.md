# CHANGELOG



## [v1.1.0](https://github.com/dornech/utils-mystuff-windows/releases/tag/v1.1.0)  (2026-06-18) 

### Bug fixes

- Corrections of GitHub Actions related to problem with Cairo library
(['8e73cab'](https://github.com/dornech/utils-mystuff-windows/commit/8e73cab69a0a42bdd7cd18a3d9bfe6c91f467f3c))
- Corrections and edits related to Python version
(['3467424'](https://github.com/dornech/utils-mystuff-windows/commit/34674240b8b7c44fe622ee4f964d45c1bc347ccf))
- Clean-up __init__.py
(['3e1ebea'](https://github.com/dornech/utils-mystuff-windows/commit/3e1ebea5257f6c54e3695c77cdd7e6c9083bc112))
- Move close_app_file from utils-mystuff to utils-mystuff-windows
(['c121da4'](https://github.com/dornech/utils-mystuff-windows/commit/c121da449342c99758a8a38672da1a50db31e2c6))

### Build system

- **deps**: Bump sigstore/gh-action-sigstore-python from 3.3.0 to 3.4.0
 (['137e2c7'](https://github.com/dornech/utils-mystuff-windows/commit/137e2c710d9903019e3b303e0c46d99420c5517e))
- **deps**: Bump codecov/codecov-action from 6 to 7
 (['7cec399'](https://github.com/dornech/utils-mystuff-windows/commit/7cec3990e52c305588a2fc6e7c8b422d6f0eb1fd))
- **deps**: Bump actions/upload-pages-artifact from 4 to 5
 (['a73069f'](https://github.com/dornech/utils-mystuff-windows/commit/a73069f0071807a2b80a3ead2a6ce6af57713ac3))
- **deps**: Bump codecov/codecov-action from 5 to 6
 (['62f2081'](https://github.com/dornech/utils-mystuff-windows/commit/62f2081d9ec447f7f9955bd4b5a9e4105908efe3))
- **deps**: Bump sigstore/gh-action-sigstore-python from 3.2.0 to 3.3.0
 (['33af1e2'](https://github.com/dornech/utils-mystuff-windows/commit/33af1e2ea0726c0c72949d5b7a2646ab6d6aacca))
- **deps**: Bump actions/deploy-pages from 4 to 5
 (['1ddd4f4'](https://github.com/dornech/utils-mystuff-windows/commit/1ddd4f4c43021da6d6c7b5f3a67a98456b8342b2))
- **deps**: Bump release-drafter/release-drafter from 6 to 7
 (['7733dba'](https://github.com/dornech/utils-mystuff-windows/commit/7733dba7e41e2068a14350c9db2f5b31bb0a4acd))
- **deps**: Bump crazy-max/ghaction-github-labeler from 5.3.0 to 6.0.0
 (['b8c0a9b'](https://github.com/dornech/utils-mystuff-windows/commit/b8c0a9bcbef7a0009bbdad3559e600e9f92e84c6))
- **deps**: Bump actions/download-artifact from 7 to 8
 (['ff96434'](https://github.com/dornech/utils-mystuff-windows/commit/ff9643477d6dce9b2dcb7c0ff438aaed7e4b053e))
- **deps**: Bump actions/upload-artifact from 6 to 7
 (['03aebd1'](https://github.com/dornech/utils-mystuff-windows/commit/03aebd1a0cb6791372b4bf1ffdcaa3786742ed63))
- **deps**: Bump actions/download-artifact from 6 to 7
 (['b2bb35c'](https://github.com/dornech/utils-mystuff-windows/commit/b2bb35cc055b624828badd905714541e89f05784))
- **deps**: Bump actions/upload-artifact from 5 to 6
 (['43c2cc8'](https://github.com/dornech/utils-mystuff-windows/commit/43c2cc80e1091357a9274f89279f1318785592c2))
- **deps**: Bump sigstore/gh-action-sigstore-python from 3.1.0 to 3.2.0
 (['e950d67'](https://github.com/dornech/utils-mystuff-windows/commit/e950d6767ebb51f3afe6cf5ac0acd01408b20403))
- **deps**: Bump actions/checkout from 5 to 6
 (['0ab6241'](https://github.com/dornech/utils-mystuff-windows/commit/0ab62414a9d12d6929c298587ee428eed9b69b61))
- Update pyproject.toml and GitHub Action for tests - minimum Python version 3.10
(['354e34a'](https://github.com/dornech/utils-mystuff-windows/commit/354e34a6c006c589b1cb582b413280dc7bb18bd6))
- **deps**: Bump sigstore/gh-action-sigstore-python from 3.0.1 to 3.1.0
 (['c97c41c'](https://github.com/dornech/utils-mystuff-windows/commit/c97c41c6e68e4f5e0ca4e93d01837299ee74c467))
- **deps**: Bump actions/download-artifact from 5 to 6
 (['9f2522b'](https://github.com/dornech/utils-mystuff-windows/commit/9f2522b0c88fdc85d78d9b0994d23baf11610d65))
- **deps**: Bump actions/upload-artifact from 4 to 5
 (['8a6c7d6'](https://github.com/dornech/utils-mystuff-windows/commit/8a6c7d6721b0e5ba3ed306f5d944b4213dc241b0))
- Additional GitHub action - test documentation build
(['56ce797'](https://github.com/dornech/utils-mystuff-windows/commit/56ce7977e68d4c377902769de225418ff90fc5bc))

### Features

- Switch from mkdocs and mkdocs-theme material to properdocs with theme materialx
(['d116bc7'](https://github.com/dornech/utils-mystuff-windows/commit/d116bc7aab2f94162b1a9b8127ca0196162784f3))
- Improve closing of files locked by an application
(['03d7f5b'](https://github.com/dornech/utils-mystuff-windows/commit/03d7f5b82fabe9ec4b25494fc1e48d00efce374b))
- Allow partial titles, check with timeout for successful close, add interface for Windows32API function AssocQuery to kill assigned application process
fix: correct find_titles via ctypes by adding required decode()
(['03d7f5b'](https://github.com/dornech/utils-mystuff-windows/commit/03d7f5b82fabe9ec4b25494fc1e48d00efce374b))

## [v1.0.0](https://github.com/dornech/utils-mystuff-windows/releases/tag/v1.0.0)  (2025-10-01) 

### Bug fixes

- Final clean-up before publication
(['7e301e3'](https://github.com/dornech/utils-mystuff-windows/commit/7e301e37370b5fe01ea86cd17d81fe2cac69e3b0))
- GitHub build actions must run on windows-latest
(['953968a'](https://github.com/dornech/utils-mystuff-windows/commit/953968a045fb5ea6490093fb41bc2e6ae2019021))
- GitHub build actions must run on windows-latest
(['38c388f'](https://github.com/dornech/utils-mystuff-windows/commit/38c388f73c68bee1773225739f69abc88b64bad6))
- Include missing coding file
(['48d2100'](https://github.com/dornech/utils-mystuff-windows/commit/48d2100a9b56be97c2f438aac21c1d601f4d9869))
- Correct generated .cruft.json
(['76bb9ca'](https://github.com/dornech/utils-mystuff-windows/commit/76bb9ca9639f03118939923582c4a0de04091c86))

### Build system

- **deps**: Bump codecov/codecov-action from 4 to 5
 (['fb46336'](https://github.com/dornech/utils-mystuff-windows/commit/fb46336f4a91fc0451be3ce1bb5e4dc9f11e98b8))
- Initial commit
(['79e9225'](https://github.com/dornech/utils-mystuff-windows/commit/79e92255f5d027adbcd98662f37e9b82fef03d1f))

### Initial commit

