## Copyright (C) 2012, 2016 Moreno Marzolla
##
## This file is part of the queueing toolbox.
##
## The queueing toolbox is free software: you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.
##
## The queueing toolbox is distributed in the hope that it will be
## useful, but WITHOUT ANY WARRANTY; without even the implied warranty
## of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with the queueing toolbox. If not, see <http://www.gnu.org/licenses/>

1; # not a function file

#Video for difference between 1MP and 8MP: https://www.youtube.com/watch?v=JgZtjfjJ4eM

page_screen_output(0); # avoid output pagination
arg_list = argv();

N1 = str2num(arg_list{1});
N2 = str2num(arg_list{2});

cores = str2num(arg_list{3});

Z1 = str2num(arg_list{4});
Scam1 = str2num(arg_list{5});
Scloud1 = str2num(arg_list{6});

Z2 = str2num(arg_list{7});
Scam2 = str2num(arg_list{8});
Scloud2 = str2num(arg_list{9});

startTime = time();

pop = [N1 N2];
#Resources: Delay -> Waiting -> Sensors -> Serverless 
D = [Z1 Scam1/cores Scloud1; #This parameters are derived from MobiSys13
   Z2 Scam2/cores Scloud2]; #This parameters are derived from MobiSys13
V = ones(size(D));
num_servers = [0, 1, 0];

[U R Q X] = qncmmva( pop, D, V, num_servers );
Uc = sum(U(:,2));
analTime = time() - startTime;

fprintf('%f,%f,%f,%f\n', X(1,1), X(2,1), Uc, analTime)


