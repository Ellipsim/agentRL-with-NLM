(define (problem problem_12)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 - block
)

(:init
	(clear obj0)
	(clear obj1)
	(clear obj2)
	(clear obj3)
	(clear obj4)
	(clear obj5)
	(clear obj6)
	(clear obj9)
	(clear obj10)
	(clear obj11)
	(clear obj12)
	(handempty)
	(on obj8 obj7)
	(on obj9 obj8)
	(ontable obj0)
	(ontable obj1)
	(ontable obj2)
	(ontable obj3)
	(ontable obj4)
	(ontable obj5)
	(ontable obj6)
	(ontable obj7)
	(ontable obj10)
	(ontable obj11)
	(ontable obj12)
)

(:goal (and
	(on obj4 obj0)
	(on obj5 obj10)
	(on obj8 obj9)
	(on obj9 obj3)
))
)