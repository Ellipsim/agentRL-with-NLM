

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(on b3 b5)
(on b4 b7)
(on b5 b9)
(ontable b6)
(ontable b7)
(on b8 b6)
(ontable b9)
(clear b1)
(clear b2)
(clear b3)
(clear b8)
)
(:goal
(and
(on b2 b6)
(on b3 b2)
(on b4 b3)
(on b5 b4)
(on b6 b7)
(on b7 b9)
(on b8 b5))
)
)


