

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b9)
(ontable b3)
(on b4 b3)
(ontable b5)
(ontable b6)
(on b7 b1)
(ontable b8)
(on b9 b7)
(clear b2)
(clear b5)
(clear b6)
(clear b8)
)
(:goal
(and
(on b1 b6)
(on b4 b2)
(on b5 b7)
(on b6 b5)
(on b7 b3)
(on b8 b9))
)
)


