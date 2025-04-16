# isp.py: I Spoof Packets with my ISP

As explained in my 2009 [Playing with DNS servers... some more](https://blog.sebastien.raveau.name/2009/02/playing-with-dns-servers-some-more.html) blog post I realized DNS caching can be leveraged to check if an Internet Service Provider lets you spoof your source IP, instead of needing another computer running tcpdump for example on the other side of the ISP.

[Firewalking](https://en.wikipedia.org/wiki/Firewalk_(computing)) would achieve the same but I was deeply honored to have my tool picked up by BackTrack (now known as Kali) and impress my inspiration [Dan Kaminsky](https://en.wikipedia.org/wiki/Dan_Kaminsky) (Black Ops of TCP/IP, 2008 DNS flaw all over mainstream news, etc; may he rest in peace) when I had the privilege to brainstorm with him at ShmooCon 2010.

Kali understandably dropped support since I never maintained my tool beyond the Proof Of Concept behind a now-broken link at my blog post so I am uploading it to GitHub at least for easy access.
