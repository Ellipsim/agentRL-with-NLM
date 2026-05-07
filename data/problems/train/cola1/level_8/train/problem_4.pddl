

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(ontable b3)
(on b4 b8)
(on b5 b7)
(ontable b6)
(on b7 b4)
(ontable b8)
(on b9 b6)
(on b10 b5)
(clear b2)
(clear b3)
(clear b9)
(clear b10)
)
(:goal
(and
(on b1 b3)
(on b2 b10)
(on b3 b7)
(on b5 b6)
(on b6 b2)
(on b8 b1)
(on b9 b8))
)
)


