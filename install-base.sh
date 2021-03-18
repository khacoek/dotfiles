#!/bin/bash

ln -sf /usr/share/zoneinfo/Asia/Jakarta /etc/localtime
hwclock --systohc
sed -i '177s/.//' /etc/locale.gen
locale-gen
locale > /etc/locale.conf
echo "KEYMAP=us" >> /etc/vconsole.conf
echo "legion" >> /etc/hostname
echo "127.0.0.1 localhost" >> /etc/hosts
echo "::1       localhost" >> /etc/hosts
echo "127.0.1.1 legion.localdomain legion" >> /etc/hosts
mkinitcpio -P
echo root:dk | chpasswd

pacman -S --noconfirm grub efibootmgr networkmanager intel-ucode tlp base-devel linux-headers pulseaudio pavucontrol brightnessctl 

pacman -S --noconfirm nvidia nvidia-settings xorg xorg-xinit

grub-install --target=x86_64-efi --efi-directory=/boot --recheck
grub-mkconfig -o /boot/grub/grub.cfg

systemctl enable NetworkManager
systemctl enable tlp

useradd -m dk
echo dk:dk | chpasswd
usermod -aG wheel,storage,audio,video dk

echo "dk ALL=(ALL) ALL" >> /etc/sudoers.d/dk


/bin/echo -e "\e[1;32mDone! Type exit, umount -R /mnt and reboot.\e[0m"




