package dev.arnv.bluke.usb

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.BufferedReader
import java.io.BufferedWriter
import java.io.InputStreamReader
import java.io.OutputStreamWriter
import java.net.InetSocketAddress
import java.net.Socket

/**
 * ADB-reverse TCP transport for the LegacyBluke Windows receiver.
 * Run adb reverse tcp:27183 tcp:27183 after authorizing USB debugging.
 * UI integration remains separate from the Bluetooth manager.
 */
class UsbDebugBridge(
    private val host: String = "127.0.0.1",
    private val port: Int = 27183,
) : AutoCloseable {
    private var socket: Socket? = null
    private var reader: BufferedReader? = null
    private var writer: BufferedWriter? = null

    suspend fun connect(): Result<Unit> = withContext(Dispatchers.IO) {
        runCatching {
            close()
            val next = Socket()
            next.connect(InetSocketAddress(host, port), 2_000)
            next.soTimeout = 2_000
            socket = next
            reader = BufferedReader(InputStreamReader(next.getInputStream(), Charsets.UTF_8))
            writer = BufferedWriter(OutputStreamWriter(next.getOutputStream(), Charsets.UTF_8))
        }
    }

    suspend fun send(event: JSONObject): Result<JSONObject> = withContext(Dispatchers.IO) {
        runCatching {
            val out = writer ?: error("USB bridge is not connected")
            val input = reader ?: error("USB bridge is not connected")
            out.write(event.toString())
            out.newLine()
            out.flush()
            val line = input.readLine() ?: error("Windows receiver disconnected")
            JSONObject(line).also {
                if (!it.optBoolean("ok", false)) error(it.optString("error", "Host rejected event"))
            }
        }
    }

    override fun close() {
        runCatching { reader?.close() }
        runCatching { writer?.close() }
        runCatching { socket?.close() }
        reader = null
        writer = null
        socket = null
    }
}
