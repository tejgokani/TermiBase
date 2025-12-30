# Homebrew formula for TermiBase
class Termibase < Formula
  desc "A terminal-native database learning playground"
  homepage "https://github.com/tejgokani/TermiBase"
  url "https://github.com/tejgokani/TermiBase/archive/refs/tags/v0.1.7.tar.gz"
  sha256 "7f3ed74b53917eb034b8d625027b72a184499db628dee5e2308506607b6ddd4a"
  version "0.1.7"
  license "MIT"

  depends_on "python@3.11"

  def install
    system "python3", "-m", "pip", "install", "--prefix=#{prefix}", "."
  end

  test do
    system "#{bin}/termibase", "--help"
  end
end
