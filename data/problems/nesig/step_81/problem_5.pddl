(define (problem problem_5)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 - block
)

(:init
	(clear obj3)
	(clear obj5)
	(clear obj7)
	(clear obj8)
	(clear obj9)
	(clear obj12)
	(handempty)
	(on obj1 obj0)
	(on obj2 obj1)
	(on obj3 obj2)
	(on obj5 obj4)
	(on obj7 obj6)
	(on obj11 obj10)
	(on obj12 obj11)
	(ontable obj0)
	(ontable obj4)
	(ontable obj6)
	(ontable obj8)
	(ontable obj9)
	(ontable obj10)
)

(:goal (and
	(on obj1 obj0)
	(on obj2 obj1)
	(on obj3 obj2)
	(on obj7 obj6)
	(on obj11 obj10)
	(on obj12 obj11)
))
)