CVM
LS SR3 SR0 3
LS SR1 SR0 1
LS SR2 SR0 2
LS SR5 SR0 4
LS SR6 SR0 5
MTCL SR1
LV VR1 SR3
LV VR2 SR3
ADD SR4 SR1 SR3
MULVV VR3 VR1 VR2
LV VR1 SR4
LV VR2 SR4
ADD SR3 SR1 SR4
MULVV VR4 VR1 VR2
ADDVV VR5 VR3 VR4
LV VR1 SR3
LV VR2 SR3
ADD SR4 SR1 SR3
MULVV VR4 VR1 VR2
ADDVV VR3 VR4 VR5
LV VR1 SR4
LV VR2 SR4
ADD SR3 SR1 SR4
MULVV VR4 VR1 VR2
ADDVV VR5 VR3 VR4
LV VR1 SR3
LV VR2 SR3
ADD SR4 SR1 SR3
MULVV VR4 VR1 VR2
ADDVV VR3 VR4 VR5
LV VR1 SR4
LV VR2 SR4
ADD SR3 SR1 SR4
MULVV VR4 VR1 VR2
ADDVV VR5 VR3 VR4
LV VR1 SR3
LV VR2 SR3
ADD SR4 SR1 SR3
MULVV VR4 VR1 VR2
ADDVV VR3 VR4 VR5
MTCL SR2
LV VR1 SR4
LV VR2 SR4
MULVV VR6 VR1 VR2
MTCL SR1
ADDVV VR5 VR6 VR3
SRL SR3 SR1 SR5
PACKLO VR4 VR5 VR0
PACKHI VR3 VR5 VR0
MTCL SR3
ADDVV VR2 VR3 VR4
SRL SR1 SR3 SR5
PACKLO VR3 VR2 VR0
PACKHI VR4 VR2 VR0
MTCL SR1
ADDVV VR1 VR3 VR4
SRL SR3 SR1 SR5
PACKLO VR3 VR1 VR0
PACKHI VR4 VR1 VR0
MTCL SR3
ADDVV VR2 VR3 VR4
SRL SR1 SR3 SR5
PACKLO VR3 VR1 VR0
PACKHI VR4 VR1 VR0
MTCL SR1
ADDVV VR1 VR3 VR4
SRL SR3 SR1 SR5
PACKLO VR3 VR1 VR0
PACKHI VR4 VR1 VR0
MTCL SR3
ADDVV VR2 VR3 VR4
SRL SR1 SR3 SR5
PACKLO VR3 VR1 VR0
PACKHI VR4 VR1 VR0
MTCL SR1
ADDVV VR1 VR3 VR4
SV VR1 SR6
HALT