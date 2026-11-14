# Changelog

## [0.9.0](https://github.com/k4black/codebleu/compare/0.8.0...0.9.0) (2026-11-14)


### ⚠ BREAKING CHANGES

* **metrics:** align scores with the CodeBLEU paper

### Features

* add `go` and `ruby` support ([#12](https://github.com/k4black/codebleu/issues/12)) ([2fc11d7](https://github.com/k4black/codebleu/commit/2fc11d7e315761d836290ee089ecc1af93277fac))
* add CPP and C langs from XLCoST ([56438b6](https://github.com/k4black/codebleu/commit/56438b6c1bd5096609e4eef50ac8487c543ce7a2))
* add dummy pkg ([4926e70](https://github.com/k4black/codebleu/commit/4926e70d7f3d18ef1ec666f13da84f9fd8bdd2e0))
* add rust lang ([#33](https://github.com/k4black/codebleu/issues/33)) ([a2e9524](https://github.com/k4black/codebleu/commit/a2e9524aaf9a5457625d0fe231b695d632a0f24e))
* add Rust parser ([#31](https://github.com/k4black/codebleu/issues/31)) ([a30cb9f](https://github.com/k4black/codebleu/commit/a30cb9f71b9c533844bd7a3e129cd83869727b03))
* add test support of evaluate lib ([d38198a](https://github.com/k4black/codebleu/commit/d38198af6d7092b7d419f4baf2f2937548c7e4bc))
* add TypeScript and Fortran and repair Rust data flow ([a03b03c](https://github.com/k4black/codebleu/commit/a03b03c9f46bb85372e94c9432c6fad42af53b14))
* add windows support and refactor setup ([#11](https://github.com/k4black/codebleu/issues/11)) ([beb64bb](https://github.com/k4black/codebleu/commit/beb64bb594f9fd2f4091d37c643b9c605519db13))
* Update for tree sitter 0.22 with prebuilt wheels ([#46](https://github.com/k4black/codebleu/issues/46)) ([acd8217](https://github.com/k4black/codebleu/commit/acd82178f75186d8d29743c14bfb8209146fa0ab))
* working staff and basic tests ([8b965cd](https://github.com/k4black/codebleu/commit/8b965cdad7030128467219e05f1f4a46d3f761d7))


### Bug Fixes

* add git so file ([d3c8bdf](https://github.com/k4black/codebleu/commit/d3c8bdf33ebeeeafe4f90b2435a61b6cfa54ca2a))
* add keywords to wheel ([311cbfa](https://github.com/k4black/codebleu/commit/311cbfa6353bd2268a1c88ca80a89976fbb5fc6a))
* Clean up code ([#1](https://github.com/k4black/codebleu/issues/1)) ([d79e2aa](https://github.com/k4black/codebleu/commit/d79e2aaad0dcbe2a705c8a9ba2f1594e151880cd))
* cloning hf repo ([cc4d98d](https://github.com/k4black/codebleu/commit/cc4d98dc346ecd6648f35445e3ffc345515521d9))
* cloning hf repo ([166f36d](https://github.com/k4black/codebleu/commit/166f36de6cb9e8e677d510ac710c95ece3b08b23))
* cloning hf repo ([0fa18f0](https://github.com/k4black/codebleu/commit/0fa18f0d2b52080b4ed8a92048db1fed9888b0e5))
* evaluate metadata ([5f3cc1a](https://github.com/k4black/codebleu/commit/5f3cc1a9a90a1edfb873da9be386554ed9800e4d))
* Make language a list in evaluate app, added comments to evaluate description ([0ad3a2b](https://github.com/k4black/codebleu/commit/0ad3a2b2a9496e1d1c6882d4beb0f2d83b6571af))
* **metrics:** align scores with the CodeBLEU paper ([9c7ec25](https://github.com/k4black/codebleu/commit/9c7ec250262d9008f0476f866aea3ebcb3e3d806))
* remove prints in calc_codebleu ([05f27e4](https://github.com/k4black/codebleu/commit/05f27e4063900e51028ac1eedf486567ce6c2916))
* to work with 3.12 and add examples tests ([#10](https://github.com/k4black/codebleu/issues/10)) ([8a944ea](https://github.com/k4black/codebleu/commit/8a944ea4e5120fd88d7c26d34ca474b3dd8fffd7))
* try to fix hf space ([a784b3f](https://github.com/k4black/codebleu/commit/a784b3f099f6eb74cee13c5b671b59838f9f161e))
* try to import codebleu using importlib ([baa97fe](https://github.com/k4black/codebleu/commit/baa97fee74f4b0eeabf3510743f6a28d0606ab5f))
* try to install codebleu from script ([b937ac6](https://github.com/k4black/codebleu/commit/b937ac6e2ebacc569482a8005b7748c90433eeae))
* try to install codebleu from script ([df5a08d](https://github.com/k4black/codebleu/commit/df5a08d2918356f0afdc2cf1843d87edd6fdcf1f))

## [0.8.0](https://github.com/k4black/codebleu/compare/0.7.1...0.8.0) (2026-11-14)


### ⚠ BREAKING CHANGES

* **metrics:** align scores with the CodeBLEU paper

### Features

* add TypeScript and Fortran and repair Rust data flow ([a03b03c](https://github.com/k4black/codebleu/commit/a03b03c9f46bb85372e94c9432c6fad42af53b14))


### Bug Fixes

* **metrics:** align scores with the CodeBLEU paper ([9c7ec25](https://github.com/k4black/codebleu/commit/9c7ec250262d9008f0476f866aea3ebcb3e3d806))

## [0.7.1](https://github.com/k4black/codebleu/releases/tag/0.7.1) (2024-05-30)

- Fix publication of the 0.7.0 package.
- Update cibuildwheel from 2.18.0 to 2.18.1 in PR #49.

[Full changes from 0.7.0 to 0.7.1](https://github.com/k4black/codebleu/compare/0.7.0...0.7.1).
