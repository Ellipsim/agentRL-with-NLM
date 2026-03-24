(define (problem problem_21)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 - block
)

(:init
	(clear obj0)
	(clear obj2)
	(clear obj8)
	(clear obj10)
	(clear obj12)
	(handempty)
	(on obj2 obj1)
	(on obj6 obj5)
	(on obj7 obj3)
	(on obj8 obj4)
	(on obj9 obj6)
	(on obj10 obj9)
	(on obj11 obj7)
	(on obj12 obj11)
	(ontable obj0)
	(ontable obj1)
	(ontable obj3)
	(ontable obj4)
	(ontable obj5)
)

(:goal (and
	(on obj0 obj11)
	(on obj2 obj4)
	(on obj4 obj10)
	(on obj6 obj5)
	(on obj7 obj3)
	(on obj8 obj0)
	(on obj9 obj6)
	(on obj10 obj9)
	(on obj11 obj7)
	(on obj12 obj8)
))
)