(define (problem problem_16)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 - block
)

(:init
	(clear obj0)
	(clear obj5)
	(clear obj7)
	(clear obj8)
	(clear obj11)
	(handempty)
	(on obj2 obj1)
	(on obj3 obj2)
	(on obj4 obj3)
	(on obj5 obj4)
	(on obj7 obj6)
	(on obj10 obj9)
	(on obj11 obj10)
	(ontable obj0)
	(ontable obj1)
	(ontable obj6)
	(ontable obj8)
	(ontable obj9)
)

(:goal (and
	(on obj2 obj1)
	(on obj3 obj2)
	(on obj4 obj3)
	(on obj5 obj4)
	(on obj7 obj6)
	(on obj10 obj9)
	(on obj11 obj10)
))
)