# Homebrew formula for TermiBase
class Termibase < Formula
  desc "A terminal-native database learning playground"
  homepage "https://github.com/tejgokani/TermiBase"
  url "https://github.com/tejgokani/TermiBase/archive/refs/tags/v0.2.3.tar.gz"
  sha256 "UPDATE_ME_WITH_REAL_SHA256_FOR_V0_2_3"
  version "0.2.3"
  license "MIT"

  depends_on "python@3.11"

  def install
    system "python3", "-m", "pip", "install", "--prefix=#{prefix}", "."
  end

  test do
    system "#{bin}/termibase", "--help"
  end
end
