# Homebrew formula for TermiBase
class Termibase < Formula
  desc "A terminal-native database learning playground"
  homepage "https://github.com/tejgokani/TermiBase"
  url "https://github.com/tejgokani/TermiBase/archive/refs/tags/v0.2.2.tar.gz"
  sha256 "2bf83e5e9a2139b4fbe36690e0ed28997ae6725ec253774a7f6192a29027a0e2"
  version "0.2.2"
  license "MIT"

  depends_on "python@3.11"

  def install
    system "python3", "-m", "pip", "install", "--prefix=#{prefix}", "."
  end

  test do
    system "#{bin}/termibase", "--help"
  end
end
