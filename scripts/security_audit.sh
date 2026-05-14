PROFILE="devsecops-user"

echo "Running DevSecOps Security Audit..."

echo -e "\n1. Attached Policies for $PROFILE:"
aws iam list-attached-user-policies --user-name $PROFILE --profile $PROFILE --output table

echo -e "\n2. Security Groups with Port 22 Open (0.0.0.0/0):"
aws ec2 describe-security-groups --filters Name=ip-permission.from-port,Values=22 Name=ip-permission.to-port,Values=22 Name=ip-permission.cidr,Values='0.0.0.0/0' --profile $PROFILE --query "SecurityGroups[*].{ID:GroupId,Name:GroupName}" --output table

echo -e "\n Audit Complete."