# Homebrew core formula for TermiBase
# This version is for submitting to homebrew-core
class Termibase < Formula
  desc "Terminal-native database learning playground"
  homepage "https://github.com/tejgokani/TermiBase"
  url "https://github.com/tejgokani/TermiBase/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "597578e4985906d15619cec83b7759cb53b74efdc4956b7f5994563e6872897e"
  license "MIT"
  head "https://github.com/tejgokani/TermiBase.git", branch: "main"

  depends_on "python@3.11"

  def install
    system "python3", "-m", "pip", "install", "--prefix=#{prefix}", "."
  end

  test do
    system "#{bin}/termibase", "--help"
  end
end

