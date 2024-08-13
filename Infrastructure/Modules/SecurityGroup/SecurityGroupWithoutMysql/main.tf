# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

/*================================
      AWS Security group
=================================*/

resource "aws_security_group" "sg" {
  name        = var.name
  description = var.description
  vpc_id      = var.vpc_id

  ingress {
    protocol        = "tcp"
    from_port       = var.ingress_port
    to_port         = var.ingress_port
    cidr_blocks     = var.cidr_blocks_ingress
    security_groups = var.security_groups
  }
  egress {
    from_port   = var.egress_port
    to_port     = var.egress_port
    protocol    = "-1"
    cidr_blocks = var.cidr_blocks_egress
  }


  tags = {
    Name = var.name
  }
}

#   resource "aws_security_group_rule" "allow_mysql" {
#   count = var.add_mysql_sg_rule  == "yes" ? 1 : 0

#   type              = "ingress"
#   from_port         = 3306
#   to_port           = 3306
#   protocol          = "tcp"
#   security_group_id = aws_security_group.sg.id
#   source_security_group_id = aws_security_group.sg.id
# }
