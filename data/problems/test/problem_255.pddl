

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(ontable b1)
(on b2 b9)
(on b3 b7)
(on b4 b11)
(on b5 b1)
(on b6 b5)
(ontable b7)
(on b8 b12)
(ontable b9)
(on b10 b6)
(on b11 b3)
(ontable b12)
(clear b2)
(clear b4)
(clear b8)
(clear b10)
)
(:goal
(and
(on b2 b3)
(on b4 b5)
(on b5 b9)
(on b6 b4)
(on b7 b12)
(on b9 b1)
(on b10 b6)
(on b12 b8))
)
)


