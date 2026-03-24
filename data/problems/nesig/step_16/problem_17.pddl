(define (problem problem_17)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 - block
)

(:init
	(clear obj0)
	(clear obj2)
	(clear obj5)
	(clear obj8)
	(clear obj9)
	(clear obj10)
	(clear obj11)
	(handempty)
	(on obj2 obj1)
	(on obj4 obj3)
	(on obj5 obj4)
	(on obj7 obj6)
	(on obj8 obj7)
	(ontable obj0)
	(ontable obj1)
	(ontable obj3)
	(ontable obj6)
	(ontable obj9)
	(ontable obj10)
	(ontable obj11)
)

(:goal (and
	(on obj0 obj8)
	(on obj4 obj3)
	(on obj5 obj4)
	(on obj7 obj6)
	(on obj8 obj9)
))
)