

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b9)
(on b2 b7)
(on b3 b1)
(ontable b4)
(ontable b5)
(ontable b6)
(on b7 b6)
(ontable b8)
(on b9 b8)
(clear b2)
(clear b3)
(clear b4)
(clear b5)
)
(:goal
(and
(on b1 b3)
(on b2 b8)
(on b3 b4)
(on b4 b6)
(on b6 b7)
(on b8 b5))
)
)


