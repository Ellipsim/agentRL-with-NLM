

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b9)
(on b3 b7)
(on b4 b5)
(on b5 b3)
(ontable b6)
(on b7 b1)
(ontable b8)
(ontable b9)
(clear b4)
(clear b6)
(clear b8)
)
(:goal
(and
(on b1 b6)
(on b2 b8)
(on b3 b4)
(on b9 b5))
)
)


