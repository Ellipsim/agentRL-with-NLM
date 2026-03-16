

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(on b2 b9)
(on b3 b8)
(on b4 b7)
(on b5 b6)
(ontable b6)
(on b7 b1)
(ontable b8)
(on b9 b4)
(clear b2)
(clear b3)
(clear b5)
)
(:goal
(and
(on b1 b7)
(on b2 b9)
(on b4 b6)
(on b5 b8)
(on b6 b3)
(on b7 b2)
(on b8 b1))
)
)


