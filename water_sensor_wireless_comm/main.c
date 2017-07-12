
#include <xdc/std.h>
#include <xdc/runtime/System.h>
#include <xdc/runtime/Log.h>

#include <ti/sysbios/BIOS.h>
#include <ti/sysbios/knl/Clock.h>
#include <ti/sysbios/knl/Task.h>


#include <ti/drivers/PIN.h>
#include <ti/drivers/GPIO.h>
#include <ti/drivers/UART.h>
#include <ti/drivers/ADC.h>


#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include "Board.h"
#include "easylink/EasyLink.h"
#include "RF_Com.h"
#include "ToServer_Com.h"


int main (void) {
    Board_initGeneral();
    
    BIOS_start();
    return 0;
}
