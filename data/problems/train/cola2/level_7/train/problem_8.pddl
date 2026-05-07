

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b8)
(ontable b2)
(on b3 b2)
(on b4 b7)
(ontable b5)
(ontable b6)
(on b7 b1)
(on b8 b6)
(ontable b9)
(clear b3)
(clear b4)
(clear b5)
(clear b9)
)
(:goal
(and
(on b1 b4)
(on b3 b5)
(on b5 b1)
(on b6 b2)
(on b7 b3)
(on b8 b9)
(on b9 b7))
)
)


