
all: lede-source/.config

LEDE_VERSION := "13e6f7a75df8d03188b3a84a12086e8fe28ed6bb"

lede-source/.config: config/lede.config
	test -d lede-source || git clone https://git.lede-project.org/source.git lede-source
	(cd lede-source ; git checkout $(LEDE_VERSION))
	cp config/lede.config lede-source/.config
	cp mac80211-patches/*.patch lede-source/package/kernel/mac80211/patches/
	(cd lede-source ; make)
