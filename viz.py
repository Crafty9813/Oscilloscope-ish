import serial
import matplotlib.pyplot as plt

PORT = '/dev/ttyACM0'
BAUD = 115200
MAX_POINTS = 500

ser = serial.Serial(PORT, BAUD, timeout=1)

data = []

plt.ion()
fig, ax = plt.subplots()

line_plot, = ax.plot([], [])

while True:
    try:
        if not plt.fignum_exists(fig.number):
            break
        
        ser.reset_input_buffer() # IMPORTANT: clear buffer to avoid lag
        line = ser.readline().decode(errors='ignore').strip()

        if line.isdigit():
            value = int(line)

            # Ignore outliers bc noise
            if len(data) > 0 and abs(value - data[-1]) > 500:
                continue

            data.append(value)

            # Keep buffer size fixed
            if len(data) > MAX_POINTS:
                data.pop(0)

            line_plot.set_xdata(range(len(data)))
            line_plot.set_ydata(data)

            ax.set_xlim(0, MAX_POINTS)
            ax.set_ylim(0, 4095) # 12-bit ADC range

            plt.draw()
            plt.pause(0.001)

    except KeyboardInterrupt:
        break

ser.close()