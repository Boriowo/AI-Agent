resource "aws_instance" "vm" {
  ami           = "ami-0430580de6244e02e"
  instance_type = "t2.micro"
  
  tags = {
    Name        = "${var.name}-${var.environment}-vm"
    Environment = var.environment
  }

  root_block_device {
    volume_size = 8
    volume_type = "gp2"
  }

  vpc_security_group_ids = [aws_security_group.vm_sg.id]
}

resource "aws_security_group" "vm_sg" {
  name        = "${var.name}-${var.environment}-vm-sg"
  description = "Security group for VM"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.name}-${var.environment}-vm-sg"
    Environment = var.environment
  }
}