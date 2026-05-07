

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(on b3 b6)
(on b4 b5)
(ontable b5)
(ontable b6)
(on b7 b2)
(ontable b8)
(on b9 b1)
(clear b3)
(clear b7)
(clear b8)
(clear b9)
)
(:goal
(and
(on b1 b5)
(on b2 b7)
(on b3 b6)
(on b4 b3)
(on b5 b4)
(on b7 b8)
(on b9 b1))
)
)


