# Homebrew formula for TermiBase
class Termibase < Formula
  desc "A terminal-native database learning playground"
  homepage "https://github.com/tejgokani/TermiBase"
  url "https://github.com/tejgokani/TermiBase/archive/refs/tags/v0.2.1.tar.gz"
  sha256 "e0a38074078261ad3111b9f1fa5c7cb58c285b2a5ea4465346641c22e42bfa99"
  version "0.2.1"
  license "MIT"

  depends_on "python@3.11"

  def install
    system "python3", "-m", "pip", "install", "--prefix=#{prefix}", "."
  end

  test do
    system "#{bin}/termibase", "--help"
  end
end
