# Homebrew formula for TermiBase
class Termibase < Formula
  desc "A terminal-native database learning playground"
  homepage "https://github.com/tejgokani/TermiBase"
  url "https://github.com/tejgokani/TermiBase.git",
      tag: "v0.1.0",
      revision: "HEAD"
  version "0.1.0"
  license "MIT"

  depends_on "python@3.11"

  def install
    system "python3", "-m", "pip", "install", "--prefix=#{prefix}", "."
  end

  test do
    system "#{bin}/termibase", "--help"
  end
end
