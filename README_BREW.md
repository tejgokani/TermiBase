# Homebrew Installation

## For Users

Install TermiBase with Homebrew:

```bash
brew tap yourusername/termibase
brew install termibase
```

Or in one command:
```bash
brew install yourusername/termibase/termibase
```

## For Developers (Setting Up)

### Option 1: Homebrew Tap (Recommended)

1. **Create tap repository:**
   ```bash
   # Create GitHub repo: homebrew-termibase
   # Name MUST start with "homebrew-"
   ```

2. **Add formula:**
   ```bash
   git clone https://github.com/yourusername/homebrew-termibase.git
   cd homebrew-termibase
   cp /path/to/TermiBase/Formula/termibase.rb .
   # Edit termibase.rb: replace "yourusername" with your GitHub username
   git add termibase.rb
   git commit -m "Add TermiBase formula"
   git push
   ```

3. **Users install:**
   ```bash
   brew tap yourusername/termibase
   brew install termibase
   ```

### Option 2: Direct Install (No Tap)

Users can install directly from your main repo:

```bash
brew install --build-from-source \
  https://raw.githubusercontent.com/yourusername/termibase/main/Formula/termibase.rb
```

### Option 3: Local Development

Test the formula locally:

```bash
brew install --build-from-source ./Formula/termibase.rb
brew test termibase
```

## Updating the Formula

When releasing a new version:

1. Create a git tag: `git tag v0.1.1`
2. Update `version` in `termibase.rb`
3. Update `tag` in `termibase.rb` to match
4. Push tag: `git push origin v0.1.1`
5. Update tap repo with new formula

## Formula File

The formula is located at: `Formula/termibase.rb`

Make sure to:
- Replace `yourusername` with your actual GitHub username
- Update `homepage` URL
- Update `url` to point to your repo

