

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b7)
(ontable b2)
(ontable b3)
(on b4 b3)
(on b5 b2)
(on b6 b8)
(on b7 b4)
(ontable b8)
(ontable b9)
(clear b1)
(clear b5)
(clear b6)
(clear b9)
)
(:goal
(and
(on b1 b6)
(on b2 b1)
(on b3 b7)
(on b5 b3)
(on b6 b9)
(on b7 b4)
(on b8 b5))
)
)


