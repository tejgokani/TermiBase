# Submitting TermiBase to Homebrew Core

To enable `brew install termibase` (without tap), you need to submit to Homebrew core.

## Prerequisites

1. **Create a GitHub release tag:**
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

2. **Calculate SHA256:**
   ```bash
   curl -L https://github.com/tejgokani/TermiBase/archive/refs/tags/v0.1.0.tar.gz | shasum -a 256
   ```

3. **Update formula with SHA256** in `Formula/termibase-core.rb`

## Steps to Submit

1. **Fork homebrew-core:**
   ```bash
   brew tap-new $USER/termibase
   ```

2. **Create formula:**
   ```bash
   brew create --python https://github.com/tejgokani/TermiBase/archive/refs/tags/v0.1.0.tar.gz
   ```

3. **Edit the formula** to match `Formula/termibase-core.rb`

4. **Test locally:**
   ```bash
   brew install --build-from-source ./Formula/termibase-core.rb
   brew test termibase
   ```

5. **Submit PR:**
   ```bash
   cd $(brew --repository homebrew/core)
   git checkout -b termibase
   # Copy formula to Formula/termibase.rb
   git add Formula/termibase.rb
   git commit -m "termibase: add formula"
   git push origin termibase
   ```
   Then create PR on GitHub: https://github.com/Homebrew/homebrew-core

## Requirements

- ✅ Formula follows Homebrew conventions
- ✅ Has a test block
- ✅ Uses stable version (tag) not just branch
- ✅ Proper dependencies
- ✅ License specified

## Alternative: Simplify Tap Command

Instead, you can make the tap easier to use:

```bash
# Users run:
brew tap tejgokani/termibase
brew install termibase  # Works after tapping!
```

This is much easier and doesn't require Homebrew approval.

