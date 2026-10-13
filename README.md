# PC Sync Server
A cross-platform file synchronization server delivering local files to an Android client.

## Overview & Motivation
Managing academic and personal workflows across multiple devices (laptops, tablets, and mobile phones) frequently leads to fragmented file storage. Manually transferring lecture slides, readings, and assignment assets between platforms is inefficient and prone to version discrepancies.

To address this friction and gain practical experience with low-level networking, this project implements a custom client-server file synchronization tool. Built using TCP/IP socket programming, the application establishes a reliable transmission channel to automate local network file transfers between a primary workstation and target mobile devices.

## Key Features
Universal File Support: Capable of transferring diverse file formats, including documents (PDFs, docs), media (audio, video), and images.

Graphical User Interface (GUI): Clean interface designed for simple connection management and visual transfer status.

One-Click Synchronization: Initiates batch file dispatching instantly across connected endpoints.

Reliable TCP Transmission: Leverages connection-oriented sockets to ensure ordered, error-checked packet delivery.

Sync History Logging: Automatically timestamps successful transfers to maintain an accurate audit log of recent updates.

## Technical Constraints & Roadmap
Current Buffer Architecture: The initial prototype employs a fixed, lightweight transfer buffer sized for typical academic documents (e.g., standard text and PDF files).

## Future Enhancements: 
Future releases will introduce dynamic buffer allocation, chunked streaming for large-scale media files, and configurable network throughput settings.
