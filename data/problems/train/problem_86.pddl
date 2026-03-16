

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(on b2 b6)
(ontable b3)
(on b4 b8)
(on b5 b1)
(on b6 b5)
(on b7 b3)
(on b8 b9)
(ontable b9)
(clear b2)
(clear b4)
(clear b7)
)
(:goal
(and
(on b1 b6)
(on b2 b5)
(on b4 b8)
(on b5 b7)
(on b8 b9))
)
)


