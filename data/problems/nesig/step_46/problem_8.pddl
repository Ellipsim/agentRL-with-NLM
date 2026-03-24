(define (problem problem_8)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 - block
)

(:init
	(clear obj0)
	(clear obj3)
	(clear obj4)
	(clear obj5)
	(clear obj6)
	(clear obj7)
	(clear obj8)
	(clear obj10)
	(clear obj11)
	(clear obj12)
	(handempty)
	(on obj2 obj1)
	(on obj3 obj2)
	(on obj10 obj9)
	(ontable obj0)
	(ontable obj1)
	(ontable obj4)
	(ontable obj5)
	(ontable obj6)
	(ontable obj7)
	(ontable obj8)
	(ontable obj9)
	(ontable obj11)
	(ontable obj12)
)

(:goal (and
	(on obj0 obj9)
	(on obj1 obj2)
	(on obj2 obj3)
	(on obj3 obj12)
	(on obj9 obj10)
	(on obj10 obj11)
))
)