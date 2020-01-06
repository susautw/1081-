import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

public class CountingJavaClient {
    public static void main(String[] args) throws Exception {
        int port = Integer.valueOf(args[0]);
        Socket socket = getSocket(port);
        System.out.println("Connection establishes ...");
        BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        System.out.println("Message sent from server: " + reader.readLine());
        socket.close();
    }

    public static Socket getSocket(int port) throws Exception {
        try {
            return new Socket("127.0.0.1", port);
        } catch (IOException e) {
            throw new Exception("Socket error");
        }
    }
}
