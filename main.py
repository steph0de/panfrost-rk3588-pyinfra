from pyinfra.operations import apt, files, server


# @deploy("Install multimedia packages for rockchip")
def rockchipMultimedia():
    files.link(
        name="Create link /usr/lib64 that points to /lib",
        path="/usr/lib64",
        target="/lib",
    )

    apt.ppa(
        name="Add the rockchip-multimedia ppa",
        src="ppa:liujianfeng1994/rockchip-multimedia",
    )

    apt.update(
        name="Update apt repositories",
        cache_time=3600,
    )

    apt.Install(
        name="Install rockchip-multimedia-config",
        packages=["rockchip-multimedia-config"],
        latest=True
    )

    if apt.packages(
        name="Install forked v4l libraries",
        packages=["libv4l-rkmpp","v4l-utils"],
        latest=True
    ).changed:
        files.link(
            name="Create link for libv4l2.so",
            path="/usr/lib64/libv4l2.so",
            target="aarch64-linux-gnu/libv4l2.so.0.0.0",
        )

# @deploy("Install Panfork Mesa to support Mali G610")
def panforkMesa():
    apt.ppa(
        name="Add the panfork-mesa ppa",
        src="ppa:liujianfeng1994/panfork-mesa",
    )
    files.download(
        name="Download/Install latest Mali g610 firmware",
        src="https://github.com/JeffyCN/rockchip_mirrors/raw/libmali/firmware/g610/mali_csffw.bin",
        dest="/lib/firmware/mali_csffw.bin",
        force=True,
    )

panforkMesa()
rockchipMultimedia()
apt.upgrade(
    name="Upgrade system",
)
apt.packages(
    name="Install other libraries",
    packages=["librockchip-vpu0"],
    latest=True
)
apt.packages(
    name="Install mpv",
    packages=["mpv"],
    latest=True
)

server.reboot(
    name="Restarting sbc"
)