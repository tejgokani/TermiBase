# Homebrew Installation Setup

## Quick Setup (5 minutes)

### Step 1: Create Homebrew Tap Repository

1. Create a new GitHub repository named `homebrew-termibase`
2. The name MUST start with `homebrew-` for Homebrew to recognize it

### Step 2: Add Formula File

1. Copy `Formula/termibase.rb` to your `homebrew-termibase` repo
2. Update the `url` and `homepage` in the formula with your actual GitHub username
3. Commit and push:

```bash
git clone https://github.com/yourusername/homebrew-termibase.git
cd homebrew-termibase
cp /path/to/TermiBase/Formula/termibase.rb .
# Edit termibase.rb to update URLs
git add termibase.rb
git commit -m "Add TermiBase formula"
git push
```

### Step 3: Calculate SHA256 (for releases)

When you create a release tag:

```bash
# After creating a release tag (e.g., v0.1.0)
curl -L https://github.com/yourusername/termibase/archive/refs/tags/v0.1.0.tar.gz | shasum -a 256
```

Update the `sha256` in the formula with this value.

### Step 4: Users Install With

```bash
brew tap yourusername/termibase
brew install termibase
```

Or in one command:
```bash
brew install yourusername/termibase/termibase
```

## Alternative: Install from GitHub Directly

If you want to skip the tap setup, users can install directly:

```bash
brew install --build-from-source --HEAD https://raw.githubusercontent.com/yourusername/termibase/main/Formula/termibase.rb
```

## Formula File Location

The formula file should be at:
- `homebrew-termibase/termibase.rb` (for tap)
- Or in your main repo at `Formula/termibase.rb` (for direct install)

## Testing Locally

Test the formula before publishing:

```bash
brew install --build-from-source ./Formula/termibase.rb
brew test termibase
```

## Updating the Formula

When you release a new version:

1. Update `version` in `termibase.rb`
2. Update `url` to point to the new release tag
3. Calculate new `sha256`
4. Commit and push to your tap repo

## Notes

- Formula installs from GitHub main branch by default
- For releases, update `url` to point to release tarball
- SHA256 is required for releases (not for HEAD installs)
- Users need Python 3.11+ (specified in formula)

