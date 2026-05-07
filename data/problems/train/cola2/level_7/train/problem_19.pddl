

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(on b3 b9)
(ontable b4)
(on b5 b8)
(ontable b6)
(on b7 b3)
(on b8 b4)
(on b9 b6)
(clear b2)
(clear b5)
(clear b7)
)
(:goal
(and
(on b2 b4)
(on b3 b2)
(on b4 b6)
(on b5 b8)
(on b6 b9)
(on b8 b7)
(on b9 b5))
)
)


