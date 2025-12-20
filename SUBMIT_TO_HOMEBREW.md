# Submit TermiBase to Homebrew Core

## ✅ Prerequisites Complete

- ✅ Release tag created: `v0.1.0`
- ✅ SHA256 calculated: `597578e4985906d15619cec83b7759cb53b74efdc4956b7f5994563e6872897e`
- ✅ Formula prepared: `Formula/termibase-core.rb`

## Steps to Submit

### 1. Fork homebrew-core

```bash
# Clone homebrew-core
git clone https://github.com/Homebrew/homebrew-core.git
cd homebrew-core
```

### 2. Create Formula File

```bash
# Copy the formula
cp /path/to/TermiBase/Formula/termibase-core.rb Formula/termibase.rb
```

Or create it directly:
```bash
# Create new formula
brew create --python https://github.com/tejgokani/TermiBase/archive/refs/tags/v0.1.0.tar.gz
# Then edit Formula/termibase.rb to match Formula/termibase-core.rb
```

### 3. Test Locally

```bash
# Test the formula
brew install --build-from-source ./Formula/termibase.rb
brew test termibase
brew uninstall termibase
```

### 4. Commit and Push

```bash
git checkout -b termibase
git add Formula/termibase.rb
git commit -m "termibase: add formula"
git push origin termibase
```

### 5. Create Pull Request

1. Go to: https://github.com/Homebrew/homebrew-core
2. Click "New Pull Request"
3. Select your fork and `termibase` branch
4. Fill out PR template
5. Submit!

## PR Template

**Title:** `termibase: add formula`

**Description:**
```
Adds TermiBase, a terminal-native database learning playground.

- Educational tool for learning SQL and database internals
- Interactive REPL with query visualization
- Execution plan visualization
- MIT licensed
```

## Formula Requirements Checklist

- ✅ Stable version (tag v0.1.0)
- ✅ SHA256 checksum included
- ✅ Proper dependencies (python@3.11)
- ✅ Test block included
- ✅ License specified (MIT)
- ✅ Homepage and URL correct

## After Approval

Once merged, users can install with:
```bash
brew install termibase
```

No tap needed! 🎉

## Notes

- Review process can take 1-4 weeks
- Homebrew maintainers may request changes
- Be responsive to feedback
- Keep the formula updated with new releases

