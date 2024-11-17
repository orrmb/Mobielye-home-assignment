#!/bin/bash




display_menu() {
	echo "Select Option:"
	echo "1) Change user permission on Repo/group "
	echo "2) Modify Item"
}

user_perm() {
	read -p "${bold}${green}${underline}Enter repo/group:${normal} " repo
    read -p "${bold}${green}${underline}Enter username:${normal} " username

    respone ="curl --header "PRIVATE-TOKEN: ${GITLABTOKEN}" "https://gitlab.com/api/v4/groups/Mobielye/members"



	if [[ -e $path ]];then
		extention="${path##*.}"
		filename="$(echo "${path}" | awk -F '/' '{print $NF}')"
		case $extention in
			jpeg|jpg|mp4|mp3)
			mkdir -p "${PERSONAL_PATH}";
			cp $path $PERSONAL_PATH;
			echo "${bold}${aqua}New file added ${normal}${filename}";;
			sh|py|yaml|yml)
			mkdir -p "${DEVELOPMENT_PATH}";
      cp $path $DEVELOPMENT_PATH ;
			echo "${bold}${aqua}New file added ${normal}${filename}";;
			doc|pdf|txt)
			echo $filename
			mkdir -p "${EDUCATION_PATH}";
      cp $path $EDUCATION_PATH ;
      echo "${bold}${aqua}New file added ${normal}${filename}";;
		esac
	else
		echo "${bold}${red}The file is not exist, Please try again...${normal}"
	fi
}

Modify(){
	read -p "${bold}${green}${underline}Enter the file path that you want modify:${normal} " path
	if [ -f $path ];then
		read -p "${bold}${green}${underline}Enter the new name:${normal} " newname
		mv $path $newname

		echo -e "${bold}${aqua}The file name changed from to${normal} ${newname}"
	else
		echo "${bold}${red}The file is not exist, Please try again...${normal}"
	fi
}

Delete(){
  read -p "${bold}${green}${underline}Which file do you want to delete? Enter path please:${normal} " path
  if [ -f $path ];then
    filename="$(echo "${path}" | awk -F '/' '{print $NF}')"
    read -p "Are you srue?(y/n)${normal}" ans
    if [[ ${ans} =~ ^[Yy] ]];then
      rm $path
      echo "${bold}${red}${underline}The file ${normal}${filename} ${bold}${red}${underline}deleted${normal}"
    else
      echo "${bold}${red}The file is not exist, Please try again...${normal}"
    fi
  fi
}

See_what(){
  read -p "${bold}${green}${underline}In which folder do you want to see the content?(personal, education, development):${normal} " choice
  if [ ${choice} == 'personal' ];then
    mkdir -p "${PERSONAL_PATH}";
    if [ "$(ls -A "${PERSONAL_PATH}" | wc -l)" -eq 0 ];then
      echo "${bold}${red}The folder is empty, Please try to add something...${normal}"
    else
      echo -e "${bold}${aqua}$(ls -A PERSONAL_PATH )${normal}\n"
    fi
  elif [ ${choice} == 'education' ]; then
      mkdir -p "${EDUCATION_PATH}";
      if [ "$(ls -A "${EDUCATION_PATH}" | wc -l)" -eq 0 ];then
        echo "${bold}${red}The folder is empty, Please try to add something...${normal}"
      else
        echo -e "${bold}${aqua}$(ls -A $EDUCATION_PATH )${normal}\n"
      fi
  elif [ ${choice} == 'development' ]; then
      mkdir -p "${DEVELOPMENT_PATH}";
      if [ "$(ls -A "${DEVELOPMENT_PATH}" | wc -l)" -eq 0 ];then
        echo "${bold}${red}The folder is empty, Please try to add something...${normal}"
      else
        echo -e "${bold}${aqua}$(ls -A $DEVELOPMENT_PATH )${normal}\n"
      fi
  else
    echo "${bold}${red}The folder is not exist, Please try again...${normal}"
  fi
}

#Path for file
PERSONAL_PATH="/home/${USERNAME}/personal"
DEVELOPMENT_PATH="/home/${USERNAME}/development"
EDUCATION_PATH="/home/${USERNAME}/education"
while true; do
	display_menu
	read -p "${bold}${underline}Enter your choice:${normal} " reply
	case $reply in
		1) user_perm ;;
		2) issues_mr ;;
        *) echo -e "${bold}${red}There is no option like this TRY AGAIN!(1-5)\n${normal}" ;;
	esac
done
#Add color
bold=$(tput bold)
green=$(tput setaf 2)
red=$(tput setaf 9)
aqua=$(tput setaf 14)
underline=$(tput smul)
normal=$(tput sgr0)